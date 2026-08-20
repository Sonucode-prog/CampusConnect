<template>
    <section class="hero-section">
        <div class="container py-5">
            <div class="row align-items-center min-vh-75">

                <!-- Left Content -->
                <div class="col-lg-6 mb-5 mb-lg-0">

                    <span class="badge bg-primary-subtle text-primary px-3 py-2 rounded-pill mb-3">
                        🎓 Smart Campus Placement Platform
                    </span>

                    <h1 class="display-3 fw-bold text-dark lh-sm">
                        Campus Placement
                        <span class="text-primary">Management</span>
                        Made Easy
                    </h1>

                    <p class="lead text-secondary mt-4 mb-4">
                        Connect students, companies, and your placement cell
                        through one powerful and easy-to-use platform.
                    </p>

                    <!-- Features -->
                    <div class="row g-3 mb-4">

                        <div class="col-sm-6">
                            <div class="d-flex align-items-center">
                                <div class="feature-icon me-2">
                                    ✓
                                </div>
                                <span>Student Management</span>
                            </div>
                        </div>

                        <div class="col-sm-6">
                            <div class="d-flex align-items-center">
                                <div class="feature-icon me-2">
                                    ✓
                                </div>
                                <span>Company Recruitment</span>
                            </div>
                        </div>

                        <div class="col-sm-6">
                            <div class="d-flex align-items-center">
                                <div class="feature-icon me-2">
                                    ✓
                                </div>
                                <span>Placement Tracking</span>
                            </div>
                        </div>

                        <div class="col-sm-6">
                            <div class="d-flex align-items-center">
                                <div class="feature-icon me-2">
                                    ✓
                                </div>
                                <span>Centralized Dashboard</span>
                            </div>
                        </div>

                    </div>

                    <!-- Buttons -->
                    <div class="d-flex flex-wrap gap-3">

                        <router-link
                            to="/login"
                            class="btn btn-primary btn-lg px-4 py-3 rounded-pill shadow-sm"
                        >
                            Get Started
                            <span class="ms-2">→</span>
                        </router-link>

                        <a
                            href="#features"
                            class="btn btn-outline-primary btn-lg px-4 py-3 rounded-pill"
                        >
                            Explore Features
                        </a>

                    </div>

                </div>

                <!-- Right Image -->
                <div class="col-lg-6">

                    <div class="hero-image-wrapper position-relative">

                        <!-- Decorative Circle -->
                        <div class="decorative-circle circle-one"></div>
                        <div class="decorative-circle circle-two"></div>

                        <img
                            src="\src\assets\groupimg.jpg"
                            alt="Students collaborating"
                            class="img-fluid hero-image"
                        />

                        <!-- Floating Card -->
                        <div class="floating-card shadow-lg">
                            <div class="d-flex align-items-center">

                                <div class="success-icon">
                                    ✓
                                </div>

                                <div class="ms-3">
                                    <small class="text-muted">
                                        Placement Status
                                    </small>

                                    <h6 class="mb-0 fw-bold">
                                        Recruitment Active
                                    </h6>
                                </div>

                            </div>
                        </div>

                        <!-- Student Card -->
                        <div class="student-card shadow-lg">
                            <div class="d-flex align-items-center">

                                <div class="student-icon">
                                    👨‍🎓
                                </div>

                                <div class="ms-2">
                                    <strong>Students</strong>
                                    <br>
                                    <small class="text-muted">
                                        Ready for opportunities
                                    </small>
                                </div>

                            </div>
                        </div>

                    </div>

                </div>

            </div>
        </div>
    </section>
</template>

<style scoped>
.hero-section {
    min-height: 90vh;
    display: flex;
    align-items: center;

    background:
        radial-gradient(
            circle at 10% 20%,
            rgba(13, 110, 253, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(111, 66, 193, 0.12),
            transparent 30%
        ),
        linear-gradient(135deg, #f8fbff 0%, #ffffff 100%);

    overflow: hidden;
}

.min-vh-75 {
    min-height: 75vh;
}

/* Heading */

.hero-section h1 {
    letter-spacing: -1px;
}

.hero-section h1 .text-primary {
    position: relative;
}

/* Feature Icons */

.feature-icon {
    width: 28px;
    height: 28px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background: #e7f1ff;
    color: #0d6efd;

    font-weight: bold;
}

/* Hero Image */

.hero-image-wrapper {
    padding: 20px;
}

.hero-image {
    width: 100%;
    height: 480px;
    object-fit: cover;

    border-radius: 30px;

    position: relative;
    z-index: 2;

    box-shadow:
        0 25px 60px rgba(0, 0, 0, 0.15);
}

/* Floating Cards */

.floating-card,
.student-card {
    position: absolute;

    background: white;

    padding: 16px 20px;

    border-radius: 16px;

    z-index: 3;
}

.floating-card {
    top: 45px;
    left: -10px;
}

.student-card {
    bottom: 45px;
    right: -10px;
}

/* Icons */

.success-icon,
.student-icon {
    width: 45px;
    height: 45px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    font-size: 20px;
}

.success-icon {
    background: #d1e7dd;
    color: #198754;
    font-weight: bold;
}

.student-icon {
    background: #e7f1ff;
}

/* Decorative Circles */

.decorative-circle {
    position: absolute;

    border-radius: 50%;

    z-index: 1;
}

.circle-one {
    width: 120px;
    height: 120px;

    background: rgba(13, 110, 253, 0.12);

    top: -20px;
    right: 30px;
}

.circle-two {
    width: 80px;
    height: 80px;

    background: rgba(111, 66, 193, 0.15);

    bottom: 20px;
    left: 0;
}

/* Mobile */

@media (max-width: 991px) {

    .hero-section {
        text-align: center;
    }

    .hero-section h1 {
        font-size: 2.8rem;
    }

    .hero-image-wrapper {
        margin-top: 30px;
    }

    .floating-card {
        left: 0;
    }

    .student-card {
        right: 0;
    }

}

@media (max-width: 576px) {

    .hero-section h1 {
        font-size: 2.2rem;
    }

    .hero-image {
        height: 350px;
    }

    .floating-card,
    .student-card {
        padding: 10px;
        font-size: 12px;
    }

}
</style>