const Browser = require('zombie');
const path = require('path');

Browser.localhost('example.com', 5000);

describe('External org ref POST', function() {

  const browser = new Browser();

  before(function(done) {
    let html_path = path.join(__dirname, 'helper', 'someorg-form.html');
    browser.visit('file://'+html_path, done);
  });

  describe('submits form from someorg site', function() {

    before(function(done) {
      browser.fill('email', 'someone@example.com');
      browser.fill('name_first', 'Some');
      browser.fill('name_last', 'One');
      browser.fill('dob', '01012000');
      browser.fill('phone', '555-555-5555');
      browser.fill('county', 'Allen');
      browser.pressButton('Register Me', done);
    });

    it('should end up on step 0 with form pre-filled', function() {
      browser.assert.url({pathname: '/'});
      browser.assert.input('form input[name=email]', 'someone@example.com')
    });

  });

});
