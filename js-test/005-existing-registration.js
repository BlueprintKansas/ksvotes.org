const Browser = require('zombie');

Browser.localhost('example.com', 5000);

describe('User fills out step0 form with existing registration', function() {

  const browser = new Browser();

  before(function() {
    return browser.visit('/');
  });

  describe('completes form', function() {

    before(function(done) {
      browser.fill('email', 'someone@example.com');
      browser.fill('name_first', 'Kris');
      browser.fill('name_last', 'Kobach');
      browser.fill('dob', '03/26/1966');
      browser.fill('phone', '555-555-5555');
      browser.select('county', 'Douglas');
      browser.pressButton('Next', done);
    });

    it('should move to change-or-apply', function() {
      browser.assert.url({pathname: '/change-or-apply/'});
    });

  });

});
