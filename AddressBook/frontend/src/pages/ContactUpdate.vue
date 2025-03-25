<template>
  <v-app-bar app dense fixed hide-on-scroll>
    <v-toolbar>
      <v-btn icon @click="goBack">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-toolbar-title>Edit Contact</v-toolbar-title>
    </v-toolbar>
  </v-app-bar>

  <v-content>
    <div style="margin-top: 64px;">
      <v-container class="d-flex justify-center">
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6">
            <v-card class="pa-4">
              <v-avatar size="100" class="mx-auto my-4">
                <v-img :src="avatarSrc"></v-img>
              </v-avatar>

              <v-form ref="form" @submit.prevent="saveContactChanges">
                <v-text-field 
                  v-model="contact.first_name" 
                  label="First Name" 
                  outlined 
                  required
                ></v-text-field>
                <v-text-field 
                  v-model="contact.last_name" 
                  label="Last Name" 
                  outlined 
                  required
                ></v-text-field>
                <v-text-field 
                  v-model="contact.email" 
                  label="Email" 
                  outlined 
                  required
                ></v-text-field>
                <v-btn block color="success" type="submit">Save Changes</v-btn>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-content>
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
  email: ''
})

const avatarSrc = computed(() => {
  const initials = `${contact.value.first_name[0]}${contact.value.last_name[0]}`
  return `https://ui-avatars.com/api/?name=${initials}&background=random&color=fff`
})

const fetchContact = async (id) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/contacts/${id}/`)
    contact.value = response.data
  } catch (error) {
    console.error('Error fetching contact:', error)
  }
}

onMounted(() => {
  const contactId = route.params.id
  fetchContact(contactId)
})

const saveContactChanges = async () => {
  try {
    const updatedContact = {
      first_name: contact.value.first_name,
      last_name: contact.value.last_name,
      email: contact.value.email
    }

    const response = await axios.put(`http://127.0.0.1:8000/api/contacts/${contact.value.id}/`, updatedContact)
    contact.value = response.data
    alert('Changes saved successfully!')
    router.push({ name: 'ContactDetails', params: { id: contact.value.id } })
  } catch (error) {
    console.error('Error saving contact:', error)
    alert('Failed to save changes.')
  }
}

const goBack = () => {
  router.push('/')
}
</script>
