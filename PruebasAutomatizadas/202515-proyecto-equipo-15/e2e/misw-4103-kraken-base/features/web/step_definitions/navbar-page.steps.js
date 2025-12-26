const { When } = require("@cucumber/cucumber");

When ('I click within the posts list', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('a[href="#/posts/"]');
    return await element.click();
});

When ('I click within the pages list', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('a[href="#/pages/"]');
    return await element.click();
});

When ('I click within the tags list', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('a[href="#/tags/"]');
    return await element.click();
});
