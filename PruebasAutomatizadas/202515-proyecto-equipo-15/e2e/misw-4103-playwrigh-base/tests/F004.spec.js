import { test, expect } from "@playwright/test";
import { AuthPage } from "../pages/auth-page.js";
import { NavbarPage } from "../pages/navbar-page.js";
import { PostPage } from "../pages/post-page.js";
import { TagPage } from "../pages/tag-page.js";
import { faker } from "@faker-js/faker";
import { ScreenshotManager } from "../utils/screenshot-manager.js";
import { hashString } from "../utils/utils.js";

// F004: Asignar etiqueta
test.describe('Assign Tag Tests', () => {
    let authPage;
    let navbarPage;
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
        await postPage.clickOnPostSettings(true);
        await postPage.clickOnGoBackToPosts(true);

        // Then
        await postPage.clickOnPostByTitle(postOrPageTitle);
        await postPage.clickOnPostSettings();
        const postTags = await postPage.getPostTags();
        expect(postTags).toContain(tagTitle);
        await screenshotManager.captureFinalStep();
    });
});
