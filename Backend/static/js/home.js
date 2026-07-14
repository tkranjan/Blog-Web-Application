document.addEventListener("DOMContentLoaded", () => {

    const postsContainer = document.getElementById("postsContainer");

    // Exit if we're not on the Home page
    if (!postsContainer) return;

    loadPosts();

});

async function loadPosts() {

    const token = localStorage.getItem("access_token");

    try {

        const response = await fetch("/api/posts/", {   // Change if needed

            method: "GET",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            credentials: "include"

        });

        if (!response.ok) {
            throw new Error("Failed to fetch posts");
        }

        const posts = await response.json();

        displayPosts(posts);

    }

    catch (error) {

        console.error(error);

        document.getElementById("postsContainer").innerHTML = `
            <div class="alert alert-danger">
                Unable to load posts.
            </div>
        `;

    }

}

function displayPosts(posts) {

    const postsContainer = document.getElementById("postsContainer");

    postsContainer.innerHTML = "";

    if (posts.length === 0) {

        postsContainer.innerHTML = `
            <div class="alert alert-info text-center">
                No posts available.
            </div>
        `;

        return;
    }

    posts.forEach(post => {

        postsContainer.innerHTML += `

        <div class="card post-card mb-4 shadow-sm">

            <div class="card-body">

                <!-- Header -->
                <div class="d-flex justify-content-between align-items-center">

                    <div class="d-flex align-items-center">

                        <img src="https://ui-avatars.com/api/?name=${post.author}&background=random"
                             class="rounded-circle me-3"
                             width="50"
                             height="50">

                        <div>

                            <h6 class="mb-0 fw-bold">
                                ${post.author}
                            </h6>

                            <small class="text-muted">
                                ${new Date(post.created_at).toLocaleDateString()}
                            </small>

                        </div>

                    </div>

                </div>

                <!-- Title -->

                <h3 class="mt-4 fw-bold">
                    ${post.title}
                </h3>

                <!-- Content -->

                <p class="text-muted mt-3">

                    ${
                        post.content.length > 180
                        ? post.content.substring(0,180) + "..."
                        : post.content
                    }

                </p>

                <hr>

                <!-- Footer -->

                <div class="d-flex justify-content-between align-items-center">

                    <div>

                        ❤️ ${post.likes.length}

                    </div>

                    <button
                        class="btn btn-primary">

                        Read More

                    </button>

                </div>

            </div>

        </div>

        `;

    });

}