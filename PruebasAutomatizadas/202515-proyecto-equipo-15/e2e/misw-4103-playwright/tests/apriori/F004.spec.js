// Imports
import { test, expect } from "@playwright/test";
import { TagPage } from "../../pages/tag-page.js";
import { AuthPage } from "../../pages/auth-page.js";
import { PagePage } from "../../pages/page-page.js";
import { PostPage } from "../../pages/post-page.js";
import { nextRecord } from "../../utils/data-pool.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { getAprioriDataPool } from "../../utils/mockaroo-client.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";

// Data pool load
const aprioriData = getAprioriDataPool("F004_apriori.json");

// F004: Asignar etiqueta
test.describe('Assign Tag Tests', () => {
    let authPage;
    let navbarPage;
    let pagePage;
    let postPage;
    let tagPage;
    let tagTitle;
    let tagDescription;
    let postOrPageTitle;
    let postOrPageContent;
    let screenshotManager;

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        
        // Index choice
        const record = nextRecord('F004', aprioriData);
        
        // Saving test info
        testInfo.dataPool = record;
        
        // Mapping fields to testInfo for reporting
        testInfo.dataPool = { 
            id: record.id,
            post_title: record.post_title, 
            post_content: record.post_content, 
            new_post_title: record.new_post_title,
            tag_title: record.tag_title,
            tag_description: record.tag_description
        };

        // Screenshot manager
        screenshotManager = new ScreenshotManager(page, testInfo);
        
        // Preparing pages
        authPage = new AuthPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);
        pagePage = new PagePage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        tagPage = new TagPage(page, screenshotManager);

        // Test data
        postOrPageTitle = testInfo.dataPool.post_title;
        postOrPageContent = testInfo.dataPool.post_content;
        tagTitle = testInfo.dataPool.tag_title;
        tagDescription = testInfo.dataPool.tag_description;

        // Navigate to page
        await page.goto("", { waitUntil: "domcontentloaded" });
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
