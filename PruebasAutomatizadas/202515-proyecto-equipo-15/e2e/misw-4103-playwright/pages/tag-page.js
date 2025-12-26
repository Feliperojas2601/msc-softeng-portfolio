import { BasePage } from './base-page.js';

export class TagPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.newTagButton = 'a[href="#/tags/new/"]';
        this.tagNameInput = 'input[data-test-input="tag-name"]';
        this.tagSlugInput = 'input[data-test-input="tag-slug"]';
        this.tagDescriptionInput = 'textarea[data-test-input="tag-description"]';
        this.tagColorInput = 'input[data-test-input="accentColor"]';
        this.saveTagButton = 'button[data-test-button="save"]';
        this.tagSelectorByName = (name) => `a.gh-list-data.gh-tag-list-title:has(h3.gh-tag-list-name:text-is("${name}"))`;
    }

    async clickOnNewTag() {
        await this.executeWithScreenshot('click_on_new_tag', async () => {
            await this.page.click(this.newTagButton);
            await this.page.waitForSelector(this.tagNameInput, { state: 'visible' });
        }); 
    }

    async setTagNameAndSlug(nameAndSlug) {
        await this.executeWithScreenshot('set_tag_name_and_slug', async () => {
            await this.page.click(this.tagNameInput);
            await this.page.fill(this.tagNameInput, nameAndSlug);
            await this.page.click(this.tagSlugInput);
            await this.page.fill(this.tagSlugInput, nameAndSlug);
        });
    }

    async setTagName(name) {
        await this.executeWithScreenshot('set_tag_name', async () => {
            await this.page.click(this.tagNameInput);
            await this.page.fill(this.tagNameInput, name);
        });
    }

    async setTagSlug(slug) {
        await this.executeWithScreenshot('set_tag_slug', async () => {
            await this.page.click(this.tagSlugInput);
            await this.page.fill(this.tagSlugInput, slug);
        });
    }

    async getTagSlugValue() {
        try {
            return await this.page.locator(this.tagSlugInput).inputValue();
        } catch (error) {
            return null;
        }
    }

    async setTagDescription(description) {
        await this.executeWithScreenshot('set_tag_description', async () => {
            await this.page.click(this.tagDescriptionInput);
            await this.page.fill(this.tagDescriptionInput, description);
        });
    }

    async clickOnSaveTag() {
        await this.executeWithScreenshot('click_on_save_tag', async () => {
            await this.page.click(this.saveTagButton);
            await this.page.waitForLoadState('networkidle');
        });
    }

    async isSaveButtonVisible() {
        try {
            return await this.page.locator(this.saveTagButton).isVisible({ timeout: 3000 });
        } catch (error) {
            return false;
        }
    }

    async isSaveButtonEnabled() {
        try {
            const button = this.page.locator(this.saveTagButton);
            const isVisible = await button.isVisible({ timeout: 3000 });
            if (!isVisible) return false;
            return await button.isEnabled();
        } catch (error) {
            return false;
        }
    }

    async getErrorMessage() {
        try {
            const errorSpan = this.page.locator('span.error p.response').first();
            const isVisible = await errorSpan.isVisible({ timeout: 3000 });
            if (!isVisible) return null;
            return await errorSpan.textContent();
        } catch (error) {
            return null;
        }
    }

    async setTagColor(color) {
        await this.executeWithScreenshot('set_tag_color', async () => {
            await this.page.click(this.tagColorInput);
            await this.page.fill(this.tagColorInput, color);
        });
    }

    async getTagColorValue() {
        try {
            return await this.page.locator(this.tagColorInput).inputValue();
        } catch (error) {
            return null;
        }
    }

    async clickOnTagByName(name) {
        await this.executeWithScreenshot('click_on_tag_by_name', async () => {
            const selector = this.tagSelectorByName(name);
            await this.page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
            await this.page.click(selector);
            await this.page.waitForSelector(this.tagNameInput, { state: 'visible' });
        });
    }
}