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

const fs = require("fs");
const path = require("path");

const sharp = require("sharp");

//Smaller cache to prevent issues with stack
// See: http://sharp.pixelplumbing.com/en/latest/install/#alpine-linux
sharp.cache( { files: 5 } );

/* GET resize image */
router.get("/:path-:source", function(req, res, next) {
  // Extract the query-parameter
  const widthString = req.query.width;
  const heightString = req.query.height;
  const format = req.query.format; // Support jpeg for now
  const filter = req.query.filter;

  const p = req.params.path;
  const source = req.params.source;

  let image;

  if (source === undefined) {
    throw new Error('Invalid input');
  } else {
    //TODO: check parameters
    image = path.join(__dirname, "../public/images", path.basename(p), path.basename(source));

    if (fs.existsSync(image) == false) {
      throw new Error('File does not exist');
    }
  }
  // Parse to integer if possible
  let width,
    height = 400;
  if (widthString) {
    width = parseInt(widthString);
  }
  if (heightString) {
    height = parseInt(heightString);
  }

  // Set the content-type of the response
  res.type('jpeg');
  let f = resize(image, 'jpeg', width, height, filter);
  if (f) {
    f.pipe(res);
  } else {
    throw new Error('Resize failed');
  }
});

function resize(filepath, format, width = 400, height = 400, filter) {
  try {
    const readStream = fs.createReadStream(filepath);

    let transform = sharp();

    if (format) {
      transform = transform.toFormat(format);
    }

    if (filter) {
      transform = transform.greyscale();
    }

    transform = transform.resize(width, height);

    return readStream.pipe(transform);
  } catch (e) {
    console.log(e);
  }
}

module.exports = router;
