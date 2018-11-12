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

/* GET home page. */
router.get("/", function(req, res, next){
  /* call out services and compile page */
  axios_client(
    "http://" +
      env.get("CATALOG_ENDPOINT").asString() +
      "/api/v1/product/6464865908071"
  )
    .then(value => {
      res.render("index", {
        title: "AnyCompany Shop",
        product: value.data,
        user: req.user
      });
    })
    .catch(error => {
      res.render("index", {
        title: "AnyCompany Shop",
        product: undefined,
        user: req.user
      });
    });
});

router.get("/static", function(req, res, next) {
  res.render("static", {
    title: "AnyCompany Shop"
  });
});

module.exports = router;
