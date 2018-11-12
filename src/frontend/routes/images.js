//
// Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this
// software and associated documentation files (the "Software"), to deal in the Software
// without restriction, including without limitation the rights to use, copy, modify,
// merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
// PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
// SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//

const router = require("express").Router();
const axios_client = require("../lib/ws_client");
const env = require("env-var");
const querystring = require("querystring");

/* GET health check */
router.get("/:imagename", function(req, res, next) {
  let uri =
    "http://" +
    env.get("IMAGE_ENDPOINT").asString() +
    "/" +
    req.params.imagename +
    "?" +
    querystring.stringify(req.query);

  axios_client(uri, { responseType: "stream" })
    .then(response => {
      res.type("jpeg");
      response.data.pipe(res);
    })
    .catch(e => {
      res.status(404).send("Image not found");
    });
});

module.exports = router;
