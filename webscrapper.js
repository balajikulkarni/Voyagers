var request = require("request"),
  cheerio = require("cheerio"),
  url = "http://www.posttestserver.com";
  
request(url, function (error, response, body) {
  if (!error) {
    var $ = cheerio.load(body),
      text  = $("body").text();
      
    console.log(text);
  } else {
    console.log("We’ve encountered an error: " + error);
  }
});
