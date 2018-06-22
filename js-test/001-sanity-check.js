const Browser = require('zombie');

Browser.localhost('example.com', 5000);

describe('User visits home page', function() {

  const browser = new Browser();

  describe('server responds', function() {
    it('returns 200', function() {
      browser.visit('/', function() {
        browser.assert.success();
      });
    });
  });

  describe('language respected', function() {
    it('returns Spanish', function() {
      browser.visit('/es/', function() {
        browser.assert.text('label', 'Primer Nombre');
      });
    });
  });

});
