function editPost(postId) {
    const contentP = document.getElementById(`content-${postId}`);
    const original = contentP.innerText;
    contentP.innerHTML = `
        <textarea id="edit-textarea-${postId}" class="form-control" rows="3">${original}</textarea>
        <button class="btn btn-primary btn-sm mt-2" onclick="saveEdit(${postId})">Save</button>
        <button class="btn btn-secondary btn-sm mt-2" onclick="cancelEdit(${postId}, \`${original.replace(/`/g, '\\`')}\`)">Cancel</button>
    `;
}

function cancelEdit(postId, original) {
    document.getElementById(`content-${postId}`).innerHTML = original;
}

function saveEdit(postId) {
    const textarea = document.getElementById(`edit-textarea-${postId}`);
    const newContent = textarea.value;
    fetch(`/edit_post/${postId}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({ content: newContent })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById(`content-${postId}`).innerHTML = newContent;
        } else if (data.error) {
            alert(data.error);
        }
    });
}

function toggleLike(postId) {
    fetch(`/toggle_like/${postId}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.like_count !== undefined) {
            // Just show the number without "Likes:" text
            document.getElementById(`like-count-${postId}`).innerText = data.like_count;
            
            // Update the heart icon based on like status
            const likeButton = document.querySelector(`.like-button[data-post-id="${postId}"]`);
            if (data.liked) {
                likeButton.innerHTML = '❤️';
            } else {
                likeButton.innerHTML = '♡';
            }
        }
    });
}

function toggleCommentSection(postId) {
    const commentSection = document.getElementById(`comment-section-${postId}`);
    if (commentSection.style.display === 'none') {
        commentSection.style.display = 'block';
        loadComments(postId);
    } else {
        commentSection.style.display = 'none';
    }
}

function loadComments(postId) {
    const commentsContainer = document.getElementById(`comments-${postId}`);
    commentsContainer.innerHTML = '<div class="text-center"><small>Loading comments...</small></div>';
    
    fetch(`/get_comments/${postId}/`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            commentsContainer.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            return;
        }
        
        if (data.comments.length === 0) {
            commentsContainer.innerHTML = '<div class="text-center"><small>No comments yet</small></div>';
            return;
        }
        
        let commentsHtml = '';
        data.comments.forEach(comment => {
            commentsHtml += `
                <div class="comment">
                    <strong>${comment.username}</strong>
                    <small class="text-muted ml-2">${comment.timestamp}</small>
                    <p class="mb-1">${comment.content}</p>
                </div>
                <hr class="comment-divider">
            `;
        });
        
        commentsContainer.innerHTML = commentsHtml;
    })
    .catch(error => {
        commentsContainer.innerHTML = '<div class="alert alert-danger">Failed to load comments</div>';
        console.error('Error loading comments:', error);
    });
}

function addComment(postId) {
    const textarea = document.getElementById(`comment-textarea-${postId}`);
    const content = textarea.value.trim();
    
    if (!content) {
        alert('Comment cannot be empty');
        return;
    }
    
    fetch(`/add_comment/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Clear the textarea
        textarea.value = '';
        
        // Reload comments to show the new one
        loadComments(postId);
    })
    .catch(error => {
        alert('Failed to add comment');
        console.error('Error adding comment:', error);
    });
}

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}