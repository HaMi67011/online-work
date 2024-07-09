// utils/qrcode.js
const QRCode = require('qrcode');

async function generateQRCode(data) {
    try {
        const qrCodeDataURL = await QRCode.toDataURL(data);
        return qrCodeDataURL;
    } catch (err) {
        console.error('Error generating QR code:', err);
        return null;
    }
}

module.exports = generateQRCode;
