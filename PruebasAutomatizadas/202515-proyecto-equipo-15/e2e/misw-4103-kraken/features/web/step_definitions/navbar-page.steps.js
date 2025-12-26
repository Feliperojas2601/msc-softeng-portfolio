const { When } = require("@cucumber/cucumber");

When ('I click within the posts list', async function () {
    // Dejamos que Ghost procese
    await this.driver.pause(3000);
    let element = await this.driver.$('a[data-test-nav="posts"]');
    await this.driver.pause(2000);
    return await element.click();
});

When ('I click within the pages list', async function () {
    // Dejamos que Ghost procese
    await this.driver.pause(3000);
    let element = await this.driver.$('a[data-test-nav="pages"]');
    await this.driver.pause(2000);
    return await element.click();
});

When ('I click within the tags list', async function () {
    // Dejamos que Ghost procese
    await this.driver.pause(3000);
    let element = await this.driver.$('a[data-test-nav="tags"]');
    await this.driver.pause(3000);
    return await element.click();
});
