import mongoose, { Schema } from 'mongoose';  

// Define the schema for the Job model  
const jobSchema = new Schema({  
    id: { type: String, required: true },  
    category: { type: String, required: true },  
    employer: { type: String, required: true },  
    description: { type: String, required: true },  
    requiredLevel: { type: Number, required: true },  
    passiveIncome: { type: Number, required: true },  
    assignState: { type: Boolean, default: false },  
});

// Create the model from the schema and interface  
const Job = mongoose.model('Job', jobSchema);

export default Job;