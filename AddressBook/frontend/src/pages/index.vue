<template>
  <v-container width="600px">
    <v-card class="justify-center" >
    <v-app-bar app dense fixed hide-on-scroll >
      <v-toolbar>
        <v-btn icon="mdi-menu"></v-btn>
        <v-toolbar-title text="Contacts"></v-toolbar-title>
        <v-btn icon="mdi-dots-vertical"></v-btn>
      </v-toolbar>
    </v-app-bar>
    <v-content>
        <div style="margin-top:64px; overflow-y:scroll"></div>
    </v-content>

    <v-list>
      <v-list-item v-for="contact in contactList" :key="contact.id">
        <router-link :to="{ name: 'ContactDetails', params: { id: contact.id } }">
          <v-card class="pa-5">
            <v-row aling="center">
              <v-col cols="12" class="d-flex align-center ga-3">
                <v-avatar size="40" class="d-flex justify-space-between align-center">
                  <v-img :src="getAvatar(contact.first_name, contact.last_name)" />
                </v-avatar>
                <div>
                  <v-list-item-title class="d-flex justify-space-between align-center">
                  {{ formatName(contact.first_name) }} {{ formatName(contact.last_name) }}
                </v-list-item-title>
                <v-list-item-subtitle class="d-flex justify-space-between align-center">
                  {{ contact.email }}
                </v-list-item-subtitle>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </router-link>
        <v-divider inset></v-divider>
      </v-list-item>
    </v-list>

    <v-fab 
      class="addcontact" 
      color="cyan-accent-2" 
      icon="mdi-plus" 
      size="50" 
      @click="goToAddContactPage"
      style="position: fixed; bottom: 100px; right: 100px;">
    </v-fab>
  </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const contactList = ref([]);

const fetchContacts = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/contacts/ ');
  contactList.value = response.data.sort((a, b) => {
    const nameA = `${a.first_name} ${a.last_name}`.toLowerCase();
    const nameB = `${b.first_name} ${b.last_name}`.toLowerCase();
    if (nameA < nameB) return -1;
    if (nameA > nameB) return 1;
    return 0;
  });
};

const goToAddContactPage = () => {
  router.push({ name: 'AddContact' });
};

const formatName = (name) => {
  if (!name) return '';
  return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
};

const getAvatar = (firstName, lastName) => {
  const initials = `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
  return `https://ui-avatars.com/api/?name=${initials}&background=random&color=fff`;
};

onMounted(() => {
  fetchContacts();
});
</script>
