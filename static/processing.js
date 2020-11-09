function thresh_binary() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let weightValue = document.getElementById('weightValue');
    let value = weightValue.getAttribute('value');
    cv.threshold(src, dst, parseInt(value), 255, cv.THRESH_BINARY);
    cv.imshow('threshOutput', dst);
    src.delete();
    dst.delete();
};
function thresh_binary_inv() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let weightValue = document.getElementById('weightValue');
    let value = weightValue.getAttribute('value');
    cv.threshold(src, dst, parseInt(value), 255, cv.THRESH_BINARY_INV);
    cv.imshow('threshOutput', dst);
    src.delete();
    dst.delete();
};
function thresh_trunc() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let weightValue = document.getElementById('weightValue');
    let value = weightValue.getAttribute('value');
    cv.threshold(src, dst, parseInt(value), 255, cv.THRESH_TRUNC);
    cv.imshow('threshOutput', dst);
    src.delete();
    dst.delete();
};
function thresh_tozero() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let weightValue = document.getElementById('weightValue');
    let value = weightValue.getAttribute('value');
    cv.threshold(src, dst, parseInt(value), 255, cv.THRESH_TOZERO);
    cv.imshow('threshOutput', dst);
    src.delete();
    dst.delete();
};
function thresh_otsu() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let gray = new cv.Mat();
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
    cv.threshold(gray, gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU);
    cv.imshow('threshOutput', gray);
    src.delete(); dst.delete(); gray.delete();
};
function thresh_triangle() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let gray = new cv.Mat();
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
    cv.threshold(gray, gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_TRIANGLE);
    cv.imshow('threshOutput', gray);
    src.delete(); dst.delete(); gray.delete();
};
function thresh_adaptive_g() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let weightValue = document.getElementById('weightValue');
    let value = weightValue.getAttribute('value');
    let gray = new cv.Mat();
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
    cv.adaptiveThreshold(gray, gray, parseInt(value), cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 3, 2);
    cv.imshow('threshOutput', gray);
    src.delete(); dst.delete(); gray.delete();
};
function thresh_adaptive_m() {
    let src = cv.imread('canvasOutput');
    let dst = new cv.Mat();
    let weightValue = document.getElementById('weightValue');
    let value = weightValue.getAttribute('value');
    let gray = new cv.Mat();
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
    cv.adaptiveThreshold(gray, gray, parseInt(value), cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, 2);
    cv.imshow('threshOutput', gray);
    src.delete(); dst.delete(); gray.delete();
};

function callback() {
    let weightValue = document.getElementById('weightValue');
    let trackbar = document.getElementById('trackbar');
    weightValue.setAttribute('value', trackbar.value);
    let thresh_type = document.getElementById('thresh_type')
    let selOpt = thresh_type.options[thresh_type.selectedIndex].value;
    if (selOpt == 'THRESH_BINARY') {
        thresh_binary();
    }
    else if (selOpt == 'THRESH_BINARY_INV') {
        thresh_binary_inv();
    }
    else if (selOpt == 'THRESH_TRUNC') {
        thresh_trunc();
    }
    else if (selOpt == 'THRESH_TOZERO') {
        thresh_tozero();
    }
    else if (selOpt == 'THRESH_OTSU') {
        thresh_otsu();
    }
    else if (selOpt == 'THRESH_TRIANGLE') {
        thresh_triangle();
    }
    else if (selOpt == 'THRESH_ADAPTIVE_GAUSSIAN') {
        thresh_adaptive_g();
    }
    else if (selOpt == 'THRESH_ADAPTIVE_MEAN') {
        thresh_adaptive_m();
    }
};