import { BasePage } from './base-page.js';

export class TagPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.newTagButton = 'a[href="#/tags/new/"]';
        this.tagNameInput = 'input#tag-name';
        this.tagSlugInput = 'input#tag-slug';
        this.tagDescriptionInput = 'textarea#tag-description';
        this.saveTagButton = 'button.gh-btn-primary';
        this.tagSelectorByName = (name) => `a.gh-list-data.gh-tag-list-title:has(h3.gh-tag-list-name:text-is("${name}"))`;
    }

    async clickOnNewTag() {
        await this.executeWithScreenshot('click_on_new_tag', async () => {
            await this.page.click(this.newTagButton);
            await this.page.waitForTimeout(1000);
        }); 
    }

    async setTagNameAndSlug(nameAndSlug) {
        await this.executeWithScreenshot('set_tag_name_and_slug', async () => {
            await this.page.click(this.tagNameInput);
            await this.page.fill(this.tagNameInput, nameAndSlug);
            await this.page.waitForTimeout(500);
            await this.page.click(this.tagSlugInput);
            await this.page.fill(this.tagSlugInput, nameAndSlug);
            await this.page.waitForTimeout(500);
        });
    }

    async setTagDescription(description) {
        await this.executeWithScreenshot('set_tag_description', async () => {
            await this.page.click(this.tagDescriptionInput);
            await this.page.fill(this.tagDescriptionInput, description);
            await this.page.waitForTimeout(500);
        });
    }

    async clickOnSaveTag() {
        await this.executeWithScreenshot('click_on_save_tag', async () => {
            await this.page.click(this.saveTagButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async clickOnTagByName(name) {
        await this.executeWithScreenshot('click_on_tag_by_name', async () => {
            const selector = this.tagSelectorByName(name);
            await this.page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
            await this.page.click(selector);
            await this.page.waitForTimeout(2000);
        });
    }
}