const mongoose = require('mongoose');
const Schema = mongoose.Schema;

//users
const userSchema = new Schema({
    username: { type: String, required: true },
    email: {
        type: String,
        required: true,
        match: [/.+@.+\..+/, 'Please enter a valid email address']
    },
    password: { type: String, required: false, minlength: 6 },
    confirmPassword: {
        type: String,
        required: false,
        validate: {
            validator: function (value) {
                return value === this.password;
            },
            message: 'Passwords do not match'
        }
    }
}, { timestamps: true });

const User = mongoose.model('user', userSchema);

module.exports = User;
