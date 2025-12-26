const { Given, When } = require("@cucumber/cucumber");
const { getCurrentPage } = require('../support/utils');
const properties = require('../../../properties.json');

Given("I run this project", async function () {
    const page = await getCurrentPage(this.driver);
    if (page == 'signin') {
        let element = await this.driver.$('input[name="identification"]');
        return await element.waitForExist({ timeout: 3000 });
    } else {
        let element = await this.driver.$('a.gh-btn-green');
        return await element.waitForExist({ timeout: 3000 });
    }
});

When("I register or login into the site with email {kraken-string}, user {kraken-string}, title {kraken-string} and password {kraken-string}", async function (email, user , blogTitle, password) {
    const page = await getCurrentPage(this.driver);
    const GHOST_BASE_URL = properties.BASEURL;
    const ALERT_SELECTOR = 'div.gh-alert-content'; 
    const SETUP_URL_ENDPOINT = '/#/setup/one/'; // Asumimos que esta es la URL de la página de registro inicial

    if (page == 'signin') {
        // Lógica de inicio de sesión (Login)
        let element = await this.driver.$('input[name="identification"]');
        await element.setValue(email);
        element = await this.driver.$('input[name="password"]');
        await element.setValue(password);
        element = await this.driver.$('button.login');
        return await element.click();

    } else { 
        // Lógica de Registro Inicial (Signup)
        let element = await this.driver.$('a.gh-btn-green');
        await element.click();
        await this.driver.pause(1000); 

        // Llenado del formulario de registro
        element = await this.driver.$('input[name="blog-title"]');
        await element.setValue(blogTitle);
        element = await this.driver.$('input[name="name"]');
        await element.setValue(user);
        element = await this.driver.$('input[name="email"]');
        await element.setValue(email);
        element = await this.driver.$('input[name="password"]');
        await element.setValue(password);
        
        // Clic en el botón de submit
        element = await this.driver.$('button[type="submit"]');
        await element.click();
        
        // Espera un momento para que la navegación o el error ocurra
        await this.driver.pause(2000);

        // **PASO CLAVE: VERIFICAR LA URL ACTUAL**
        const currentUrl = await this.driver.getUrl();

        if (currentUrl.includes(SETUP_URL_ENDPOINT)) {
            // Caso 1: La URL sigue siendo la de registro (Fallo de registro/Alerta esperada)
            console.log("Aún en la página de registro. Buscando alerta.");

            const alert = await this.driver.$(ALERT_SELECTOR);
            
            // Intenta esperar la alerta, si aparece significa que el usuario ya existe
            const alertExists = await alert.waitForExist({ 
                timeout: 3000, 
                reverse: false 
            }).catch(() => false);

            if (alertExists) {
                console.log("Alerta de usuario existente detectada. Redireccionando a Sign In.");
                
                // Redirecciona a la página de inicio de sesión para el login
                await this.driver.url(`${GHOST_BASE_URL}/#/signin`);

                let loginEmail = await this.driver.$('input[name="identification"]');
                await loginEmail.waitForExist({ timeout: 5000 });
                await loginEmail.setValue(email);

                let loginPassword = await this.driver.$('input[name="password"]');
                await loginPassword.setValue(password);

                let loginButton = await this.driver.$('button.login');
                return await loginButton.click();
            } else {
                 // Si sigue en la URL de setup pero no hay alerta, puede ser otro tipo de error. Se puede detener o continuar.
                 // Por ahora, solo termina la función.
                 return;
            }

        } else {
            // Caso 2: La URL ha cambiado (Registro Exitoso, ahora en el Onboarding)
            console.log("Registro exitoso. Continuar con el flujo de Onboarding.");

            let skipButton = await this.driver.$('button.gh-flow-skip');
            
            // Intenta esperar por el botón de saltar (parte del flujo de Onboarding)
            if (await skipButton.waitForExist({ timeout: 5000 }).catch(() => false)) { 
                await skipButton.click();
                
                // Espera para la redirección final al dashboard
                return await this.driver.pause(2000); 
            }
            
            // Si no hay botón de saltar, se asume que se ha llegado al destino final (dashboard).
            return;
        }
    }
});