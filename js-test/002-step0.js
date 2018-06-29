const Browser = require('zombie');

Browser.localhost('example.com', 5000);

describe('User fills out step0 form', function() {

  const browser = new Browser();

  before(function() {
    return browser.visit('/');
  });

  describe('completes form', function() {

    before(function(done) {
      browser.fill('email', 'someone@example.com');
      browser.fill('name_first', 'Some');
      browser.fill('name_last', 'One');
      browser.fill('dob', '01012000'); // intentionally not the placeholder format
      browser.fill('phone', '555-555-5555');
      browser.select('county', 'Allen');
      browser.pressButton('Next', done);
    });

    it('should move to step 1', function() {
      browser.assert.url({pathname: '/vr/citizenship'});
    });

  });

});
