import { BasePage } from './base-page.js';

export class LoginPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.emailInput = 'input[name="identification"]';
        this.passwordInput = 'input[name="password"]';
        this.loginButton = 'button.login';
    }

    async login() {
        await this.executeWithScreenshot('login', async () => {
            const email = process.env.EMAIL;
            const password = process.env.PASSWORD;
            if (!email || !password) {
                throw new Error('EMAIL and PASSWORD environment variables must be set');
            }
            await this.page.fill(this.emailInput, email);
            await this.page.fill(this.passwordInput, password);
            await this.page.click(this.loginButton);
            await this.page.waitForTimeout(4000);
        });
    }
}
