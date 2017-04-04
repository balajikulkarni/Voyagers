var request = require("request");
var cheerio = require("cheerio");
var fs = require("fs");
  url = "http://posttestserver.com";
  
request(url, function (error, response, body) {
  if (!error) {
    var $ = cheerio.load(body),
      text  = $("body").text();
      
    fs.appendFileSync('Postserver.txt',text);
	console.log("Done!");
  } else {
    console.log("We’ve encountered an error: " + error);
  }
});
