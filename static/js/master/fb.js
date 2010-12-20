function publishRec(title) {
  FB.ui({
    method: 'stream.publish',
    message: title,
    action_links: [{
      text: 'Manage movies on CinEight',
      href: 'http://apps.facebook.com/cineight/'
    }],
    user_message_prompt: 'Tell your friends about this movie:'
  });
}