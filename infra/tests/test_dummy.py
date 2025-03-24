from playwright.sync_api import expect

def test_dummy(page):
    page.goto(("https://google.com"))
    expect(page).to_have_url("github.com")