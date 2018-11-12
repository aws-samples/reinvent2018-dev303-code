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
const axios = require("axios");
const env = require("env-var");

/* GET cart page. */
router.get("/", function(req, res, next) {
  var cart_products = {};

  var user_id = req.sessionID;

  axios_client(
    "http://" + env.get("CART_ENDPOINT").asString() + "/api/v1/cart/" + user_id
  )
    .then(value => {
      cart_products = value.data;

      var promises = [];

      cart_products["items"].forEach(function(item) {
        var promise = axios_client(
          "http://" +
            env.get("CATALOG_ENDPOINT").asString() +
            "/api/v1/product/" +
            item
        );

        promises.push(promise);
      });

      var cart = [];
      var cart_value = 0;

      axios
        .all(promises)
        .then(
          axios.spread(function() {
            // Both requests are now complete
            const args = Array.from(arguments);
            args.forEach(elem => {
              let product = elem.data;
              cart_value += product["offer"]["price"];
              cart.push(elem.data);
            });

            req.session.cart = cart;
            req.session.cart_value = cart_value;

            res.render("cart", {
              title: "AnyCompany Shop",
              cart_length: cart.length,
              cart_products: cart,
              cart_value: cart_value,
              user: req.user
            });
          })
        )
        .catch(error => {
          //console.log(error.message);
          next(error);
        });
    })
    .catch(error => {
      //console.log(error.message);
      next(error);
    });
});

router.post("/", function(req, res) {
  var product_id = req.body["product_id"];

  if (product_id === "") res.status(404).end();

  var cart_id = req.sessionID;

  if (cart_id === undefined) res.sendStatus(404);

  // retrieve
  var add_to_cart = {
    product_id: product_id,
    cart_id: cart_id
  };

  axios_client
    .post(
      "http://" + env.get("CART_ENDPOINT").asString() + "/api/v1/cart",
      add_to_cart
    )
    .then(resp => {
      req.session.sessionFlash = {
        type: "success",
        message: "Product added to cart"
      };
      res.redirect("/cart");
    })
    .catch(error => {
      //console.log(error);
      req.session.sessionFlash = {
        type: "danger",
        message: "Product could not be added to cart"
      };
      res.redirect("/cart");
    });
});

/* checkout flow */
router.get("/checkout", function(req, res) {
  var order_process = req.session.order_process;

  req.session.order_process = order_process;

  let cart = [];
  let cart_value = 0.0;

  if (req.session.cart !== undefined) {
    cart = req.session.cart;
    cart_value = req.session.cart_value;
  }

  res.render("cart_summary", {
    title: "AnyCompany Shop -Checkout Summary",
    cart_length: cart.length,
    cart_products: cart,
    cart_value: cart_value,
    order: order_process,
    user: req.user
  });
});

router.post("/checkout", function(req, res, next) {
  var username = "";

  if (req.user) {
    username = req.user.username;
  }

  // Create order and store in session
  var create_order = {
    name: req.body["name"],
    email: req.body["email"],
    address: req.body["address"],
    address2: req.body["address2"],
    country: req.body["country"],
    state: req.body["state"],
    zip: req.body["zip"],
    city: req.body["city"],
    paymentMethod: req.body["paymentMethod"],
    cart_id: req.sessionID,
    user_id: req.sessionID
  };

  req.session.order_process = create_order;

  res.redirect("/cart/checkout");
});

/* Order flow */
router.get("/order", function(req, res, next){
  var order_status = req.session.order_status;

  res.render("order", {
    title: "AnyCompany Shop - Order completed",
    order: order_status,
    user: req.user
  });
});

router.post("/order", function(req, res) {
  let order_status = {};

  // retrieve
  var order_process = req.session.order_process;
  var cart_id = order_process["cart_id"];

  var uri = "http://" + env.get("ORDER_ENDPOINT").asString() + "/api/v1/order";
  axios_client
    .post(uri, order_process)
    .then(value => {
      order_status = value.data;
      req.session.order_status = order_status;

      if (order_status["code"] == 200) {
        // clear cart
        axios_client
          .delete(
            "http://" +
              env.get("CART_ENDPOINT").asString() +
              "/api/v1/cart/" +
              cart_id
          )
          .then(v => {
            // Clear from session
            delete req.session.order_process;
            delete req.session.cart;
            delete req.session.cart_value;

            res.redirect("/cart/order");
          })
          .catch(function(error) {
            //console.log(error);
            req.session.sessionFlash = {
              type: "danger",
              message: "Could not process order"
            };
            res.redirect("/cart/checkout");
          });
      }
    })
    .catch(error => {
      req.session.sessionFlash = {
        type: "danger",
        message: "Could not process order"
      };
      res.redirect("/cart/checkout");
    });
});

module.exports = router;
