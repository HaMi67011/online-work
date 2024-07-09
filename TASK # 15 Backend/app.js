const mongoURI = 'mongodb+srv://hamzaansari6060:MCoGLKAyr90uiWIQ@sna.cw74cqx.mongodb.net/?retryWrites=true&w=majority&appName=Sna';
const express = require('express');
const http = require('http');
const mongoose = require('mongoose');
const User = require('./model/db_schema');
const Admin = require('./model/admin_schema'); // Import Admin schema

const app = express();
const server = http.createServer(app);

// Middleware to parse incoming JSON and form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Connect to MongoDB
mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
  .then(() => {
    console.log('MongoDB Connected');
  })
  .catch(err => {
    console.error('MongoDB Connection Error:', err);
  });

// Route to handle POST request from signup form
app.post('/signup', async (req, res) => {
  const { username, email, password, confirmPassword } = req.body;

  try {
    // Validate inputs
    if (!username || !email || !password || !confirmPassword) {
      return res.status(400).json({ message: 'All fields are required' });
    }
    if (password !== confirmPassword) {
      return res.status(400).json({ message: 'Passwords do not match' });
    }

    // Check if email already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: 'Email is already in use' });
    }

    // Create a new user instance
    const newUser = new User({
      username,
      email,
      password,
      confirmPassword
    });

    // Save the user to the database
    await newUser.save();

    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    console.error('Error registering user:', error);
    res.status(500).json({ message: 'Failed to register user' });
  }
});

// POST endpoint for admin sign-in
app.post('/adminsignin', async (req, res) => {
  const { username, password } = req.body;

  console.log(username);
  console.log(password);

  try {
    const admin = await Admin.findOne({ username, password });
    if (!admin) {
      return res.status(400).json({ message: 'Invalid username or password for admin.' });
    }

    // Admin authentication successful
    // Set session or JWT token as needed

    // Redirect to admin dashboard on success
    res.redirect('/admin_dashboard.html');
  } catch (error) {
    console.error('Error signing in admin:', error);
    res.status(500).json({ message: 'Failed to sign in admin.' });
  }
});

// POST endpoint for user sign-in
app.post('/usersignin', async (req, res) => {
  const { username, password } = req.body;

  console.log(username);
  console.log(password);

  try {
    const user = await User.findOne({ username, password });
    if (!user) {
      return res.status(400).json({ message: 'Invalid username or password.' });
    }

    // User authentication successful
    // Set session or JWT token as needed

    // Redirect to user dashboard or homepage on success
    res.redirect('/index.html');
  } catch (error) {
    console.error('Error signing in user:', error);
    res.status(500).json({ message: 'Failed to sign in user.' });
  }
});

// Serve the signup.html file
app.get('/signup', (req, res) => {
  res.sendFile(__dirname + '/signup.html');
});

// Route to handle GET request for signin.html
app.get('/signin', (req, res) => {
  res.sendFile(__dirname + '/signin.html');
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
