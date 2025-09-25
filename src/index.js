import { createWorker } from "django-worker";

export default {
  async fetch(request, env, ctx) {
    return createWorker({
      settingsModule: "config.settings", 
    }).fetch(request, env, ctx);
  }
}