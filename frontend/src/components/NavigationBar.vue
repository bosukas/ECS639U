<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <!-- navigation brand -->
            <router-link class="navbar-brand" :to="{name: 'Main Page'}">Your Newspaper</router-link>

            <!-- navigation bar -->
            <ul class="navbar-nav">
                <li class="nav-item">
                    <router-link class="nav-link" :to="{name: 'Main Page'}">Home</router-link>
                </li>
                <li class="nav-item" v-if="userStore.user !== null">
                    <router-link class="nav-link" :to="{name: 'Other Page'}">All</router-link>
                </li>
            </ul>

            <!-- displayed when user is logged in -->
            <div v-if="userStore.user !== null">
                <router-link class="btn btn-outline-secondary" :to="{name: 'Profile Page'}">Profile</router-link>
                <button @click="onLogout()" class="btn btn-outline-danger">Logout</button>
            </div>

            <!-- displayed when user is logged out -->
            <div v-else>
                <a href="/auth/register" class="btn btn-outline-secondary">Register</a>
                <a href="/auth/login" class="btn btn-outline-success">Login</a>
            </div>
        </div>
    </nav>
</template>

<script lang="ts">
import { useUserStore } from "@/store/userStore";

export default {
    data() {
        const userStore = useUserStore()

        return {
            userStore,
            onLogout: () => {
                userStore.logout();
                this.$router.replace({'name': 'Main Page'})
            }
        }
    }
}
</script>