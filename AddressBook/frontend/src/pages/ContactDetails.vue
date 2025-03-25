<template>
  <v-app-bar app dense fixed hide-on-scroll>
    <v-toolbar>
      <v-btn icon @click="goBack">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-toolbar-title>{{ formattedFirstName }} {{ formattedLastName }}</v-toolbar-title>
    </v-toolbar>
  </v-app-bar>

  <div style="margin-top: 64px;">
  <v-container class="d-flex justify-center">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-4">
          <v-btn icon @click="openEditDialog" class="edit-btn" color="green" style="position: absolute; top: 16px; left: 16px;">
            <v-icon class="ContactUpdate">mdi-pencil</v-icon>
          </v-btn>

          <v-btn icon @click="deleteContact" class="delete-btn" color="red" style="position: absolute; top: 16px; right: 16px;">
            <v-icon>mdi-delete</v-icon>
          </v-btn>

          <v-card-text>
            <v-avatar size="70" class="mx-auto my-4 d-flex justify-center align-center text-h6" color="red">
              {{ formattedFirstName[0] }}{{ formattedLastName[0] }}
            </v-avatar>
            <v-card-title class="text-center">
              {{ formattedFirstName }} {{ formattedLastName }}
            </v-card-title>
            <v-card-subtitle class="text-center">
              {{ contact.email }}
            </v-card-subtitle>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text>
            <h3>Contact Info</h3>
            <v-list>
              <v-list-item v-for="(contactNumber, index) in contact.contact_numbers" :key="contactNumber.id">
                <v-list>
                  <v-list-item-title>{{ contactNumber.contact_type }}</v-list-item-title>
                  <v-list-item-subtitle>{{ contactNumber.contact_number }}</v-list-item-subtitle>
                </v-list>
              </v-list-item>
            </v-list>
          </v-card-text>

          <v-row justify="center" class="mt-4">
            <v-col cols="5">
              <v-btn block color="primary" @click="sendEmail(contact.email)">
                <v-icon left>mdi-email</v-icon> Send Email
              </v-btn>
            </v-col>
            <v-col cols="5">
              <v-btn block color="secondary" @click="makeCall(contact.contact_numbers[0]?.contact_number)">
                <v-icon left>mdi-phone</v-icon> Call
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</div>

  <v-dialog v-model="dialog" max-width="800">
    <v-card>
      <v-card-title>Edit Contact Info</v-card-title>

      <v-card-text>

        <v-text-field v-model="editedContact.first_name" label="First Name" required></v-text-field>
        <v-text-field v-model="editedContact.last_name" label="Last Name" required></v-text-field>
        <v-text-field v-model="editedContact.email" label="Email" required></v-text-field>

        <v-divider></v-divider>

        <v-card-title>Contact Numbers</v-card-title>
        <v-btn color="green" @click="addNewContactNumber" :disabled="editedContact.contact_numbers.length >= 3">Add New Contact</v-btn>
        
        <v-list>
          <v-list-item v-for="(contactNumber, index) in editedContact.contact_numbers" :key="index">
            <v-list-item-title class="d-flex align-center ga-3">
              <v-select v-model="contactNumber.contact_type" :items="availableContactTypes" label="Contact Type" required></v-select>
              <v-text-field v-model="contactNumber.contact_number" label="Contact Number" required :rules="[
                value => !!value || 'Contact number is required',
                value => /^\d+$/.test(value) || 'Only numbers are allowed',
                value => 10 <= value.length <= 10 || 'length is 10 digits'
              ]"
                maxlength="10"
                type="tel">
              </v-text-field>
              <v-btn icon :disabled="editedContact.contact_numbers.length === 1" @click="deleteContactNumber(index)" color="randomColor">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-list-item-title>
          </v-list-item>
        </v-list>

      </v-card-text>
      

      <v-card-actions>
        <v-btn text @click="closeDialog">Cancel</v-btn>
        <v-btn :disabled="!valid" color="primary" @click="saveChanges">Save</v-btn>
      </v-card-actions>
      
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const contact = ref({
  first_name: '',
  last_name: '',
  email: '',
  contact_numbers: [{ contact_type: '', contact_number: '' }]
})

const contactTypes = ['Home', 'Work', 'Other']
const dialog = ref(false)

const editedContact = ref({ ...contact.value })

const isEditMode = ref(false)

const fetchContact = async (id) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/contact-details/${id}/`)
    contact.value = response.data
    isEditMode.value = true
  } catch (error) {
    console.error('Error fetching contact:', error)
  }
}

const formattedFirstName = computed(() => {
  return contact.value.first_name.charAt(0).toUpperCase() + contact.value.first_name.slice(1).toLowerCase()
})

const formattedLastName = computed(() => {
  return contact.value.last_name.charAt(0).toUpperCase() + contact.value.last_name.slice(1).toLowerCase()
})

const goBack = () => {
  router.push('/')
}

const sendEmail = (email) => {
  window.location.href = `mailto:${email}`
}

const makeCall = (phoneNumber) => {
  if (phoneNumber) {
    window.location.href = `tel:${phoneNumber}`
  } else {
    alert('No phone number available to call.')
  }
}

const openEditDialog = () => {
  editedContact.value = { ...contact.value }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
}

const saveChanges = async () => {
  const dataToSend = {
    first_name: editedContact.value.first_name,
    last_name: editedContact.value.last_name,
    email: editedContact.value.email,
    contact_numbers: editedContact.value.contact_numbers,
  }

  try {
    await axios.put(`http://127.0.0.1:8000/api/contacts/${contact.value.id}/`, dataToSend)
    
    fetchContact(contact.value.id)

    closeDialog()

    router.push({ name: 'contact-update', params: { id: contact.value.id } })
  } catch (error) {
    console.error('Error updating contact:', error)
  }
}

const deleteContactNumber = (index) => {
  editedContact.value.contact_numbers.splice(index, 1)
}

const addNewContactNumber = () => {
  const newContactNumber = { contact_type: '', contact_number: '' }
  editedContact.value.contact_numbers.push(newContactNumber)
}

const deleteContact = async () => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/contacts/${contact.value.id}/`)
    router.push('/')
  } catch (error) {
    console.error('Error deleting contact:', error)
    alert('Failed to delete contact.')
  }
}


const valid = computed(() => {
  if (!isEditMode.value) {
    const firstNameValid = !!editedContact.value.first_name
    const lastNameValid = !!editedContact.value.last_name
    const emailValid = !!editedContact.value.email && /\S+@\S+\.\S+/.test(editedContact.value.email)
    const contactNumbersValid = editedContact.value.contact_numbers.every(
      (contactNumber) => contactNumber.contact_type && contactNumber.contact_number && /^\d{10}$/.test(contactNumber.contact_number)
    )

    return firstNameValid && lastNameValid && emailValid && contactNumbersValid
  } else {
    const contactNumbersValid = editedContact.value.contact_numbers.every(
      (contactNumber) => contactNumber.contact_type && contactNumber.contact_number && /^\d{10}$/.test(contactNumber.contact_number)
    )
    return contactNumbersValid
  }
})

const availableContactTypes = computed(() => {
  const usedTypes = editedContact.value.contact_numbers.map(contact => contact.contact_type)
  return contactTypes.filter(type => !usedTypes.includes(type))
})

onMounted(async () => {
  const contactId = route.params.id
  if (contactId) {
    await fetchContact(contactId)
  }
})
</script>