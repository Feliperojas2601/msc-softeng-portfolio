export class BasePage {
    constructor(page, screenshotManager = null) {
        this.page = page;
        this.screenshotManager = screenshotManager;
    }

    async executeWithScreenshot(stepName, action) {
        if (this.screenshotManager) {
            await this.screenshotManager.captureStep(stepName);
        }
        return await action();
    }
}