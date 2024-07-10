// Required modules
const express = require('express');
const path = require('path');
const PDFDocument = require('pdfkit');
const qr = require('qrcode'); // QR code generator library

// Create Express app
const app = express();
const port = 3000;

// Middleware for parsing JSON and urlencoded form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Route for serving the HTML form (index.html)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'item-create.html'));
});

// POST route for handling form submission and PDF generation
app.post('/create-item', async (req, res) => {
    try {
        // Extract form data from request body
        const formData = {
            destAddr: req.body.destAddr,
            srcAddr: req.body.srcAddr,
            itemCount: parseInt(req.body.itemCount),
            weight: parseFloat(req.body.weight),
            length: parseFloat(req.body.length),
            width: parseFloat(req.body.width),
            height: parseFloat(req.body.height)
        };

        // Convert form data and QR code to PDF using pdfkit
        const pdfBytes = await generatePDF(formData);

        // Set headers for PDF download
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', 'attachment; filename=item_details.pdf');

        // Send the generated PDF as a response
        res.send(pdfBytes);
    } catch (error) {
        console.error('Error generating PDF:', error);
        res.status(500).send('Error generating PDF.');
    }
});

// Function to generate PDF using pdfkit
async function generatePDF(data) {
    return new Promise(async (resolve, reject) => {
        try {
            // Create a new PDF document
            const doc = new PDFDocument();

            // Example: Add content to the PDF
            doc.text(`Destination Address: ${data.destAddr}`);
            doc.text(`Source Address: ${data.srcAddr}`);
            doc.text(`Item Count: ${data.itemCount}`);
            doc.text(`Weight: ${data.weight} lbs`);
            doc.text(`Dimensions: ${data.length} x ${data.width} x ${data.height} inches`);

            // Generate QR code with form data
            const qrData = JSON.stringify(data);
            const qrCodeImage = await qr.toBuffer(qrData, { errorCorrectionLevel: 'H' });

            // Embed QR code image into the PDF
            doc.image(qrCodeImage, {
                fit: [250, 250],
                align: 'center',
                valign: 'center'
            });

            // Stream the PDF document into a buffer (Uint8Array)
            const buffers = [];
            doc.on('data', buffers.push.bind(buffers));
            doc.on('end', () => {
                const pdfBytes = Buffer.concat(buffers);
                resolve(pdfBytes);
            });
            doc.end();
        } catch (error) {
            reject(error);
        }
    });
}

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
