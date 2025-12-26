const fs = require('fs');
const path = require('path');

class ScreenshotManager {
    constructor(driver, scenarioName, featureName) {
        this.driver = driver;
        this.stepCounter = {};
        this.scenarioName = this.sanitizeFileName(scenarioName);
        this.featureName = this.sanitizeFileName(featureName);
        this.screenshotsDir = path.join(
            process.cwd(),
            'screenshots-vrt',
            this.featureName,
            this.scenarioName
        );
        this.ensureDirectoryExists();
    }

    sanitizeFileName(name) {
        return name
            .replace(/[^a-z0-9]/gi, '_')
            .replace(/_+/g, '_')
            .toLowerCase();
    }

    ensureDirectoryExists() {
        if (!fs.existsSync(this.screenshotsDir)) {
            fs.mkdirSync(this.screenshotsDir, { recursive: true });
        }
    }

    async captureStep(stepName) {
        const sanitizedStepName = this.sanitizeFileName(stepName);
        if (!this.stepCounter[sanitizedStepName]) {
            this.stepCounter[sanitizedStepName] = 1;
        } else {
            this.stepCounter[sanitizedStepName]++;
        }
        const counter = this.stepCounter[sanitizedStepName];
        const totalSteps = Object.values(this.stepCounter).reduce((a, b) => a + b, 0);
        const paddedTotal = String(totalSteps).padStart(2, '0');
        const suffix = counter > 1 ? `_${counter}` : '';
        const filename = `step_${paddedTotal}_${sanitizedStepName}${suffix}.png`;
        const filepath = path.join(this.screenshotsDir, filename);
        try {
            await this.driver.saveScreenshot(filepath);
            console.log(`📸 [${this.scenarioName}] ${filename}`);
            return {
                path: filepath,
                stepName: sanitizedStepName,
                stepNumber: totalSteps,
                scenario: this.scenarioName,
                feature: this.featureName
            };
        } catch (error) {
            console.error(`❌ Error capturing screenshot: ${error.message}`);
            return null;
        }
    }

    async captureFinalStep() {
        return this.captureStep('final_step');
    }

    getScreenshotsDirectory() {
        return this.screenshotsDir;
    }
}

module.exports = { ScreenshotManager };