import { LoginPage } from './login-page.js';
import { RegisterPage } from './register-page.js';
import { BasePage } from './base-page.js';

export class AuthPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.loginPage = new LoginPage(page);
        this.registerPage = new RegisterPage(page);
    }

    async loginOrRegister() {
        await this.executeWithScreenshot('login_or_register', async () => {
            // Wait for navigation to complete and get URL
            await this.page.waitForLoadState('domcontentloaded');
            const currentUrl = this.page.url();
            
            if (currentUrl.includes('/setup') || currentUrl.includes('/setup/one')) {
                await this.registerPage.register();
            } else if (currentUrl.includes('/signin')) {
                await this.loginPage.login();
            } else if (currentUrl.includes('/dashboard') || currentUrl.includes('#/')) {
                // Already logged in, do nothing
                return;
            } else {
                // Wait a bit and check again in case redirect is in progress
                await this.page.waitForLoadState('networkidle');
                const finalUrl = this.page.url();
                
                if (finalUrl.includes('/setup') || finalUrl.includes('/setup/one')) {
                    await this.registerPage.register();
                } else if (finalUrl.includes('/signin')) {
                    await this.loginPage.login();
                } else if (finalUrl.includes('/dashboard') || finalUrl.includes('#/')) {
                    // Already logged in after redirect
                    return;
                } else {
                    console.log(`Current URL: ${finalUrl}`);
                    throw new Error(`Unknown page state for login or registration. URL: ${finalUrl}`);
                }
            }
        });
    }
}
