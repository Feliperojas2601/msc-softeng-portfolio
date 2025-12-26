// Imports
import { faker } from "@faker-js/faker";
import { test, expect } from "@playwright/test";
import { TagPage } from "../../pages/tag-page.js";
import { hashString } from "../../utils/utils.js";
import { AuthPage } from "../../pages/auth-page.js";
import { PagePage } from "../../pages/page-page.js";
import { PostPage } from "../../pages/post-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";

// F004: Asignar etiqueta
test.describe('Assign Tag Tests', () => {
    let authPage;
    let navbarPage;
    let pagePage;
    let postPage;
    let tagPage;
    let postOrPageTitle;
    let postOrPageContent;
    let tagTitle;
    let tagDescription;
    let screenshotManager;

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        const testTitle = testInfo.title;
        const testHash = hashString(testTitle);
        const baseSeed = process.env.FAKER_SEED ? Number.parseInt(process.env.FAKER_SEED) : 42;
        const uniqueSeed = baseSeed + testHash;
        faker.seed(uniqueSeed);
        screenshotManager = new ScreenshotManager(page, testInfo);
        authPage = new AuthPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);
        pagePage = new PagePage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        tagPage = new TagPage(page, screenshotManager);
        postOrPageTitle = faker.lorem.sentence();
        postOrPageContent = faker.lorem.paragraphs();
        tagTitle = faker.lorem.word();
        tagDescription = faker.lorem.sentence();

        await page.goto("", { waitUntil: "domcontentloaded" });
        await page.waitForTimeout(2000);
    });

    // E011: Asignar etiqueta a publicación
    test('Assign tag to post successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postOrPageTitle);
        await postPage.setPostContent(postOrPageContent);
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);
        await navbarPage.clickOnTags();
        await tagPage.clickOnNewTag();
        await tagPage.setTagNameAndSlug(tagTitle);
        await tagPage.setTagDescription(tagDescription);
        await tagPage.clickOnSaveTag();
        await navbarPage.clickOnPosts();
        await postPage.clickOnPostByTitle(postOrPageTitle);
        await postPage.clickOnPostSettings();
        await postPage.assignTagToPost(tagTitle);

        // Then
        const postTags = await postPage.getPostTags();
        expect(postTags).toContain(tagTitle);
        await screenshotManager.captureFinalStep();
    });

    // E012: Asignar etiqueta a página
    test('Assign tag to page successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPages();
        await pagePage.clickOnNewPage();
        await pagePage.setPageTitle(postOrPageTitle);
        await pagePage.setPageContent(postOrPageContent);
        await pagePage.clickOnPublishPage();
        await pagePage.clickOnContinueAfterPublish();
        await pagePage.clickOnRightNowPublishPage();
        await pagePage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);
        await navbarPage.clickOnTags();
        await tagPage.clickOnNewTag();
        await tagPage.setTagNameAndSlug(tagTitle);
        await tagPage.setTagDescription(tagDescription);
        await tagPage.clickOnSaveTag();
        await navbarPage.clickOnPages();
        await pagePage.clickOnPageByTitle(postOrPageTitle);
        await pagePage.openPageSettings();
        await pagePage.assignTagToPage(tagTitle);
        await pagePage.closePageSettings();
        await pagePage.clickOnGoBackToPages();

        // Then
        await pagePage.clickOnPageByTitle(postOrPageTitle);
        await pagePage.openPageSettings();
        const pageTags = await pagePage.getPageTags();
        expect(pageTags).toContain(tagTitle);
        await screenshotManager.captureFinalStep();
    });
});
