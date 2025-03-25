<template>
  <v-app-bar app dense fixed hide-on-scroll>
    <v-toolbar>
      <v-btn icon @click="goBack">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-toolbar-title text="Add New Contact"></v-toolbar-title>
    </v-toolbar>
  </v-app-bar>
  <v-container class="d-flex justify-center align-center" style="min-height: 100vh;">
    <v-card class="pa-5" width="800px">
      <v-card-title>Create New Contact</v-card-title>
      
      <v-form v-model="valid" @submit.prevent="addContact">
        <v-text-field
          v-model="newContact.first_name"
          label="First Name"
          required
        ></v-text-field>
        
        <v-text-field
          v-model="newContact.last_name"
          label="Last Name"
          required
        ></v-text-field>
        
        <v-text-field
          v-model="newContact.email"
          label="Email"
          type="email"
          required
        ></v-text-field>

        <v-divider></v-divider>
        
        <v-card-title>Contact Numbers</v-card-title>
        <v-btn 
          @click="addContactNumber" 
          color="green" 
          class="mt-4" 
          :disabled="newContact.contact_numbers.length >= 3"
        >
          Add New Contact
        </v-btn>
        
        <v-list-item v-for="(contact, index) in newContact.contact_numbers" :key="index" >
          <v-list-item-title class="d-flex align-center ga-3">
            <v-select
              v-model="contact.contact_type"
              :items="availableContactTypes"
              label="Contact Type"
              required
            ></v-select>
          
            <v-text-field
              v-model="contact.contact_number"
              label="Contact Number"
              required
              :rules="[
                  value => !!value || 'Contact number is required',
                  value => /^\d+$/.test(value) || 'Only numbers are allowed',
                  value => 10 <= value.length <= 10 || 'Length must be 10 digits'
                ]"
                maxlength="10"
              type="tel"
            ></v-text-field>
            <v-btn icon :disabled="newContact.contact_numbers.length === 1" color="red" @click="removeContactNumber(index)" text><v-icon>mdi-delete</v-icon></v-btn>
          </v-list-item-title>
          <v-col cols="12" class="mt-2"></v-col>
        </v-list-item>

        <v-card-actions class="d-flex justify-end mt-5" color="primary">
          <v-btn @click="goBack" color="secondary">Cancel</v-btn>
          <v-btn :disabled="!isFormValid" @click="addContact" color="primary">Save <v-icon icon="mdi-checkbox-marked-circle" end></v-icon></v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const valid = ref(false);
const newContact = ref({
  first_name: '',
  last_name: '',
  email: '',
  contact_numbers: [{ contact_type: '', contact_number: '' }]
});

const contactTypes = ['Home', 'Work', 'Other'];

const addContact = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/contacts/', newContact.value);
    router.push('/');
  } catch (error) {
    if (error.response && error.response.status === 400) {
      const errorMessage = error.response.data.detail || 'A contact with this name already exists.';
      alert(errorMessage);
    } else {
      console.error('Error adding contact:', error);
    }
  }
};

const addContactNumber = () => {
  newContact.value.contact_numbers.push({ contact_type: '', contact_number: '' });
};

const removeContactNumber = (index) => {
  newContact.value.contact_numbers.splice(index, 1);
};

const isFormValid = computed(() => {
  const hasValidContactNumbers = newContact.value.contact_numbers.every(contact => {
    return (
      contact.contact_type &&
      contact.contact_number &&
      /^\d{10}$/.test(contact.contact_number)
    );
  });

  return (
    valid.value &&
    newContact.value.first_name &&
    newContact.value.last_name &&
    newContact.value.email &&
    hasValidContactNumbers
  );
});

const availableContactTypes = computed(() => {
  const usedTypes = newContact.value.contact_numbers.map(contact => contact.contact_type);
  return contactTypes.filter(type => !usedTypes.includes(type));
});

const goBack = () => {
  router.push('/');
};
</script>
