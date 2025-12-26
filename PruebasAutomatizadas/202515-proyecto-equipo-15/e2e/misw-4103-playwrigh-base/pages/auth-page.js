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
            const currentUrl = this.page.url();
            await this.page.waitForTimeout(4000);
            if (currentUrl.includes('/setup') || currentUrl.includes('/setup/one')) {
                await this.registerPage.register();
                await this.page.waitForTimeout(4000);
            } else if (currentUrl.includes('/signin')) {
                await this.loginPage.login();
                await this.page.waitForTimeout(4000);
            } else {
                throw new Error('Unknown page state for login or registration');
            }
        });
    }
}
