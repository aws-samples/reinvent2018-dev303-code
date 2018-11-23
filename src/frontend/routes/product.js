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
const AWSXRay = require('aws-xray-sdk-core');
const env = require("env-var");

/* GET list of all products. */
router.get("/", function(req, res, next) {
  axios_client
    .get(
      "http://" + env.get("CATALOG_ENDPOINT").asString() + "/api/v1/products"
    )
    .then(function(value) {
      res.render("products", {
        title: "AnyCompany Shop - All Products",
        product: value.data,
        user: req.user
      });
    })
    .catch(error => {
      //log but ignore error
      //console.log(error.message)
      next(error);
    });
});

router.get("/:id", function(req, res, next) {
  var product_id = req.params["id"];

  let segment = AWSXRay.getSegment()
  segment.addAnnotation('ProductID', product_id);

  try {
    axios_client
      .get(
        "http://" +
          env.get("CATALOG_ENDPOINT").asString() +
          "/api/v1/product/" +
          product_id
      )
      .then(value => {
        var products = value.data;

        // fetch recommendations next, ignore errors here
        axios_client
          .get(
            "http://" +
              env.get("RECOMMENDER_ENDPOINT").asString() +
              "/api/v1/recommender/" +
              product_id
          )
          .then(v => {
            var rec = v.data['recommendations'];
            render(res, req, products, rec);
          })
          .catch(error => {
            console.log(error);
            render(res, req, products, undefined);
          });
      })
      .catch(e => {
        //console.log(e.message)
        next(e);
      });
  } catch (e) {
    //console.log(e.message)
    next(e); //Fail if we could not fetch product data;
  }
});

function render(res, req, products, recommendations) {
  res.render("product", {
    title: "AnyCompany Shop",
    product: products,
    recommendations: recommendations,
    user: req.user
  });
}

module.exports = router;