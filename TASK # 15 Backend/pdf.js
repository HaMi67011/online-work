//npm install pdfkit

const PDFDocument = require('pdfkit');
const fs = require('fs');

function createPDF(itemData, qrCodeDataURL, filePath) {
    const doc = new PDFDocument();

    doc.pipe(fs.createWriteStream(filePath));

    doc.fontSize(12).text('Item Details:', { underline: true }).moveDown();
    doc.text(`Destination Address: ${itemData.destAddr}`).moveDown();
    doc.text(`Source Address: ${itemData.srcAddr}`).moveDown();
    doc.text(`Item Count: ${itemData.itemCount}`).moveDown();
    doc.text(`Weight: ${itemData.weight}`).moveDown();
    doc.text(`Dimensions: ${JSON.stringify(itemData.dimensions)}`).moveDown();
    doc.text(`Shipping Date: ${itemData.shippingDate}`).moveDown();
    doc.text(`Label: ${itemData.label}`).moveDown();
    doc.text(`Price: ${itemData.price}`).moveDown();

    doc.moveDown().text('QR Code:').moveDown();
    doc.image(qrCodeDataURL, { width: 200 });

    doc.end();
}

module.exports = createPDF;
