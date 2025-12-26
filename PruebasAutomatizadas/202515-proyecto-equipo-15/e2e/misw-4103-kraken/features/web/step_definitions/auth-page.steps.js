const { Given, When } = require("@cucumber/cucumber");
const { getCurrentPage } = require('../support/utils');
const properties = require('../../../properties.json');

const ALERT_SELECTOR = 'div.gh-alert-content';

Given("I run this project", async function () {
    
    const page = await getCurrentPage(this.driver);

    if (page == 'signin') {
        let element = await this.driver.$('input[name="identification"]');        
        // Dejamos que Ghost procese
        await this.driver.pause(4000);
        return await element.waitForExist({ timeout: 3000 });

    } else {
        let element = await this.driver.$('input[name="blog-title"]');
        // Dejamos que Ghost procese
        await this.driver.pause(4000);
        return await element.waitForExist({ timeout: 3000 });
    }
});

When("I register or login into the site with email {kraken-string}, user {kraken-string}, title {kraken-string} and password {kraken-string}", 
  async function (email, user , blogTitle, password) {

    await this.driver.pause(2000);
    const page = await getCurrentPage(this.driver);
    const GHOST_BASE_URL = properties.BASEURL;
    const SETUP_URL_ENDPOINT = '/#/setup/one/'; // ajusta si tu Ghost 5.130 usa otra ruta

    if (page == 'signin') {
        // ==========================
        // LOGIN EN GHOST 5.130
        // ==========================
        let element = await this.driver.$('input[name="identification"]');
        await element.setValue(email);

        element = await this.driver.$('input[name="password"]');
        await element.setValue(password);

        // En 5.130 usas data-test-button="sign-in"
        element = await this.driver.$('[data-test-button="sign-in"]');
        await element.click();

        // Dejamos que Ghost procese
        await this.driver.pause(4000);

    } else { 
        // ==========================
        // REGISTRO EN GHOST 5.130
        // ==========================

        // En 5.130 ya estás en la pantalla con blog-title, no necesitas a.gh-btn-green
        await this.driver.pause(2000);
        let element = await this.driver.$('input[name="blog-title"]');
        await element.setValue(blogTitle);

        element = await this.driver.$('input[name="name"]');
        await element.setValue(user);

        element = await this.driver.$('input[name="email"]');
        await element.setValue(email);

        element = await this.driver.$('input[name="password"]');
        await element.setValue(password);

        // Botón de setup en Ghost 5.130
        element = await this.driver.$('[data-test-button="setup"]');
        await element.click();

        // Dejamos que Ghost procese
        await this.driver.pause(4000);

        // ==========================
        // PASO CLAVE: REVISAR URL ACTUAL
        // ==========================
        const currentUrl = await this.driver.getUrl();

        if (currentUrl.includes(SETUP_URL_ENDPOINT)) {
            // Seguimos en setup → algo falló (ej: usuario ya existe)
            console.log("Aún en la página de registro en Ghost 5.130. Buscando alerta...");

            // Dejamos que Ghost procese
            await this.driver.pause(2000);
            const alert = await this.driver.$(ALERT_SELECTOR);

            await this.driver.pause(2000);
            const alertExists = await alert.waitForExist({timeout: 3000, reverse: false}).catch(() => false);

            if (alertExists) {
                console.log("Alerta detectada en Ghost 5.130. Redireccionando a Sign In...");

                // Redirigimos al login
                await this.driver.url(`${GHOST_BASE_URL}/#/signin`);
                
                // Dejamos que Ghost procese
                await this.driver.pause(2500);

                let loginEmail = await this.driver.$('input[name="identification"]');
                await loginEmail.waitForExist({ timeout: 5000 });
                await loginEmail.setValue(email);

                let loginPassword = await this.driver.$('input[name="password"]');
                await loginPassword.setValue(password);

                let loginButton = await this.driver.$('[data-test-button="sign-in"]');
                await loginButton.click();

                // Dejamos que Ghost procese
                await this.driver.pause(4000);

            } else {
                // Sigue en setup pero sin alerta → otro tipo de fallo, no forzamos nada
                return;
            }

        } else {
            // La URL cambió → asumimos registro exitoso (onboarding / dashboard)
            console.log("Registro exitoso en Ghost 5.130. Continuando flujo...");            
            // Dejamos que Ghost procese
            await this.driver.pause(4000);
            return;
        }
    }
});