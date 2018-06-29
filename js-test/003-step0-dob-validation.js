const Browser = require('zombie');

Browser.localhost('example.com', 5000);

describe('User under 16', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/', done);
  });

  describe('enters dob', function() {

    before(function(done) {
      let thisYear = new Date().getFullYear();
      browser.fill('email', 'someone@example.com');
      browser.fill('name_first', 'Some');
      browser.fill('name_last', 'One');
      browser.fill('dob', '0101'+thisYear);
      browser.fill('phone', '555-555-5555');
      browser.select('county', 'Allen');
      browser.pressButton('Next', done);
    });

    it('should prevent form submission', function() {
      browser.assert.url({pathname: '/'});
    });

  });

});
