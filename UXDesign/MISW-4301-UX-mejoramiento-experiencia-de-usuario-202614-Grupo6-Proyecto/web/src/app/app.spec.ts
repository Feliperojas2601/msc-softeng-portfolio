// Libraries
import { App } from './app';
import { TestBed } from '@angular/core/testing';

describe('App', () => { beforeEach(async () => { await TestBed.configureTestingModule({ imports: [App], }).compileComponents(); });

  // Test that title in the app bar renders correctly
  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  // Test that title in the app bar renders correctly
  it('should render title', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, snoozeless-web');
  });
});
