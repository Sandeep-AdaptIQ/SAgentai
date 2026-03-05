/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { Disposable } from '../../../../base/common/lifecycle.js';
import { CancellationToken } from '../../../../base/common/cancellation.js';
import { getErrorMessage } from '../../../../base/common/errors.js';
import { IExtensionGalleryService, IExtensionManagementService } from '../../../../platform/extensionManagement/common/extensionManagement.js';
import { ILogService } from '../../../../platform/log/common/log.js';
import { IProductService } from '../../../../platform/product/common/productService.js';
import { IStorageService, StorageScope, StorageTarget } from '../../../../platform/storage/common/storage.js';

const defaultGalleryExtensionsInitStatusKey = 'initializing-default-gallery-extensions';

export class DefaultGalleryExtensionsInitializer extends Disposable {
	constructor(
		@IExtensionGalleryService private readonly extensionGalleryService: IExtensionGalleryService,
		@IExtensionManagementService private readonly extensionManagementService: IExtensionManagementService,
		@IStorageService storageService: IStorageService,
		@ILogService private readonly logService: ILogService,
		@IProductService private readonly productService: IProductService,
	) {
		super();

		if (storageService.getBoolean(defaultGalleryExtensionsInitStatusKey, StorageScope.APPLICATION, true)) {
			storageService.store(defaultGalleryExtensionsInitStatusKey, true, StorageScope.APPLICATION, StorageTarget.MACHINE);
			this.initializeDefaultGalleryExtensions().then(() => storageService.store(defaultGalleryExtensionsInitStatusKey, false, StorageScope.APPLICATION, StorageTarget.MACHINE));
		}
	}

	private async initializeDefaultGalleryExtensions(): Promise<void> {
		const extensionIds = this.productService.defaultGalleryExtensions;
		if (!extensionIds || extensionIds.length === 0) {
			this.logService.debug('No default gallery extensions configured');
			return;
		}

		if (!this.extensionGalleryService.isEnabled()) {
			this.logService.warn('Extension gallery is not enabled, skipping default gallery extensions installation');
			return;
		}

		this.logService.info('Installing default gallery extensions:', extensionIds.join(', '));

		try {
			const extensionInfos = extensionIds.map(id => ({ id }));
			const galleryExtensions = await this.extensionGalleryService.getExtensions(extensionInfos, CancellationToken.None);

			if (galleryExtensions.length === 0) {
				this.logService.warn('No gallery extensions found for the configured default extensions');
				return;
			}

			await Promise.all(galleryExtensions.map(async extension => {
				try {
					this.logService.info('Installing default gallery extension:', extension.identifier.id);
					await this.extensionManagementService.installFromGallery(extension, { donotIncludePackAndDependencies: true });
					this.logService.info('Default gallery extension installed:', extension.identifier.id);
				} catch (error) {
					this.logService.error('Error installing default gallery extension', extension.identifier.id, getErrorMessage(error));
				}
			}));

			this.logService.info('Default gallery extensions initialization complete');
		} catch (error) {
			this.logService.error('Error initializing default gallery extensions', getErrorMessage(error));
		}
	}
}
