import mongoose, { Schema } from 'mongoose';

const userSchema: Schema = new Schema({  
    userName: { type: String, required: true },  
    userId: { type: String, required: true },  
    avatar: { type: String, required: false },  
    coins: { type: Number, default: 0 },  
    power: { type: Number, default: 1000 },  
    data: { type: Number, default: 0 },  
    gpus: { type: Number, default: 0 },  
    levels: { type: Number, default: 0 },  
    agents: [
        {  
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Agent' // Update this to your Agent schema reference  
        }  
    ],  
    referrals: [
        {  
            type: mongoose.Schema.Types.ObjectId,  
            ref: 'User'  
        }  
    ]  
});  

const User = mongoose.model('User', userSchema);  

export default User;