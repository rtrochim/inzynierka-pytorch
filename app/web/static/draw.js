const canvas = document.querySelector("#boardCanvas");
let context = canvas.getContext("2d");
const canvas_width = canvas.width;
const canvas_height = canvas.height;
const border = 50;

const half_board_width = (canvas_width - 4 * border) / 2;
const half_board_height = (canvas_height - 2 * border);
const half_board_right_start = 3 * border + half_board_width;
const point_width = half_board_width / 6;
const point_height = canvas_height * 4.5 / 10;
context.font = "25px Arial";
const radius = point_width / 2;

const ODD_POINT_COLOR = '#743424';
const EVEN_POINT_COLOR = '#f3eada';
const BACKGROUND_CANVAS_COLOR = '#959590';
const INNER_FILL_COLOR = '#bb2c2c'
const STROKE_COLOR = '#000000'
const CANVAS_FILL_COLOR = '#000000'

const PLAYER_COLOR = '#ffffff'
const ENEMY_COLOR = '#000000'

function drawBoard() {
    context.strokeStyle = STROKE_COLOR;
    context.lineWidth = 2;

    // Canvas background
    context.fillStyle = BACKGROUND_CANVAS_COLOR;
    context.fillRect(0, 0, canvas.width, canvas.height);

    // left half
    context.fillStyle = INNER_FILL_COLOR;
    context.fillRect(border, border, half_board_width, half_board_height);

    // right half
    context.fillStyle = INNER_FILL_COLOR;
    context.fillRect(half_board_right_start, border, half_board_width, half_board_height);

    // middle line
    context.beginPath();
    context.moveTo(canvas_width / 2, 0);
    context.lineTo(canvas_width / 2, canvas_height);
    context.stroke()

    // left half border
    context.beginPath();
    context.moveTo(border, border);
    context.lineTo(border + half_board_width, border);
    context.lineTo(border + half_board_width, canvas_height - border);
    context.lineTo(border, canvas_height - border);
    context.lineTo(border, border);
    context.stroke()

    // right half border
    context.beginPath();
    context.moveTo(half_board_right_start, border);
    context.lineTo(half_board_right_start + half_board_width, border);
    context.lineTo(half_board_right_start + half_board_width, canvas_height - border);
    context.lineTo(half_board_right_start, canvas_height - border);
    context.lineTo(half_board_right_start, border);
    context.stroke()

    drawTopLeftPoints();
    drawTopRightPoints();
    drawBottomLeftPoints();
    drawBottomRightPoints();

}

function drawTopLeftPoints() {
    for (let i = 0; i < 6; i++) {
        context.beginPath();
        context.moveTo(border + i * point_width, border);
        context.lineTo(border + i * point_width + (point_width / 2), point_height);
        context.lineTo(border + (i + 1) * point_width, border);
        if (i % 2 === 0) {
            context.fillStyle = ODD_POINT_COLOR;
        } else {
            context.fillStyle = EVEN_POINT_COLOR;
        }
        context.fill();
        context.stroke()
        context.fillStyle = CANVAS_FILL_COLOR;
        context.fillText((12 + i).toString(), border + i * point_width + 5, border - 5);
    }

}

function drawTopRightPoints() {
    for (let i = 0; i < 6; i++) {
        context.beginPath();
        context.moveTo(half_board_right_start + i * point_width, border);
        context.lineTo(half_board_right_start + i * point_width + (point_width / 2), point_height);
        context.lineTo(half_board_right_start + (i + 1) * point_width, border);
        context.stroke();
        if (i % 2 === 0) {
            context.fillStyle = ODD_POINT_COLOR;
        } else {
            context.fillStyle = EVEN_POINT_COLOR;
        }
        context.fill();
        context.stroke()
        context.fillStyle = CANVAS_FILL_COLOR;
        context.fillText((18 + i).toString(), half_board_right_start + i * point_width + 5, border - 5);
    }
}

function drawBottomLeftPoints() {
    for (let i = 0; i < 6; i++) {
        context.beginPath();
        context.moveTo(border + i * point_width, canvas_height - border);
        context.lineTo(border + i * point_width + (point_width / 2), canvas_height - point_height);
        context.lineTo(border + (i + 1) * point_width, canvas_height - border);
        context.stroke();
        if (i % 2 === 0) {
            context.fillStyle = EVEN_POINT_COLOR;
        } else {
            context.fillStyle = ODD_POINT_COLOR;
        }
        context.fill();
        context.stroke()
        context.fillStyle = CANVAS_FILL_COLOR;
        if (11 - i < 10) {
            context.fillText((11 - i).toString(), border + i * point_width + 15, canvas_height - border + 25);
        } else {
            context.fillText((11 - i).toString(), border + i * point_width + 5, canvas_height - border + 25);
        }
    }
}

function drawBottomRightPoints() {
    for (let i = 0; i < 6; i++) {
        context.beginPath();
        context.moveTo(half_board_right_start + i * point_width, canvas_height - border);
        context.lineTo(half_board_right_start + i * point_width + (point_width / 2), canvas_height - point_height);
        context.lineTo(half_board_right_start + (i + 1) * point_width, canvas_height - border);
        if (i % 2 === 0) {
            context.fillStyle = EVEN_POINT_COLOR;
        } else {
            context.fillStyle = ODD_POINT_COLOR;
        }
        context.fill();
        context.stroke()
        context.fillStyle = CANVAS_FILL_COLOR;
        context.fillText((5 - i).toString(), half_board_right_start + i * point_width + 15, canvas_height - border + 25);

    }
}

function drawAllCheckers(board, bar, off) {
    drawBoard()
    board?.forEach((data, point) => {
            let checkers = data[0]
            let player = data[1]

            if (player == null) {
                return;
            }
            let text_color = 'black'
            let checkers_color = PLAYER_COLOR
            if (player === 1) {
                text_color = 'white'
                checkers_color = ENEMY_COLOR
            }
            if (0 <= point && point < 6) {
                let coord_start = {'x': half_board_right_start, 'y': canvas_height - border}
                let shift = coord_start.x + point_width * (5 - point)
                draw_point_checkers(checkers, shift, coord_start, checkers_color, text_color, 'bottom')
            }
            if (6 <= point && point < 12) {
                let coord_start = {'x': border, 'y': canvas_height - border}
                let shift = coord_start.x + point_width * (11 - point)
                draw_point_checkers(checkers, shift, coord_start, checkers_color, text_color, 'bottom')
            }
            if (12 <= point && point < 18) {
                let coord_start = {'x': border, 'y': border}
                let shift = coord_start.x + point_width * (point - 12)
                draw_point_checkers(checkers, shift, coord_start, checkers_color, text_color, 'top')
            }
            if (18 <= point && point < 24) {
                let coord_start = {'x': half_board_right_start, 'y': border}
                let shift = coord_start.x + point_width * (point - 18)
                draw_point_checkers(checkers, shift, coord_start, checkers_color, text_color, 'top')
            }
        }
    )
    draw_bar(bar)
    draw_off(off)
}

function draw_point_checkers(checkers, shift, coord_start, checkers_color, text_color, side) {
    for (let i = 0; i < checkers; i++) {
        let y = side === 'bottom' ? (coord_start.y - radius - 2 * i * radius) : (coord_start.y + radius + 2 * i * radius)
        context.beginPath();
        context.arc(shift + radius, y, radius, 0, 2 * Math.PI);
        context.fillStyle = checkers_color;
        context.fill();
        context.strokeStyle = text_color;
        context.stroke()
        if (i >= 4) {
            context.fillStyle = text_color;
            context.fillText(checkers, shift + radius - 10, y + 10);
            break;
        }
    }
}

function draw_off(off) {
    let off_white = off[0]
    let off_black = off[1]
    let coord_start = {'x': canvas_width - border, 'y': border};
    for (let i = 0; i < off_black; i++) {
        context.beginPath();
        context.arc(coord_start.x + radius, coord_start.y + radius + 2 * i * radius, radius, 0, 2 * Math.PI);
        context.fillStyle = CANVAS_FILL_COLOR;
        context.fill();
        context.strokeStyle = 'white';
        context.stroke()
        if (i >= 3) {
            context.fillStyle = 'white';
            context.fillText(off_black, coord_start.x + radius - 15, coord_start.y + radius + 2 * i * radius + 10);
            break;
        }
    }

    coord_start = {'x': canvas_width - border, 'y': canvas_height - border};
    for (let i = 0; i < off_white; i++) {
        context.beginPath();
        context.arc(coord_start.x + radius, coord_start.y - radius - 2 * i * radius, radius, 0, 2 * Math.PI);
        context.fillStyle = 'white';
        context.fill();
        context.strokeStyle = CANVAS_FILL_COLOR;
        context.stroke()
        if (i >= 3) {
            context.fillStyle = CANVAS_FILL_COLOR;
            context.fillText(off_white, coord_start.x + radius - 10, coord_start.y - radius - 2 * i * radius + 10);
            break;
        }
    }
}

function draw_bar(bar) {
    let bar_white = bar[0]
    let bar_black = bar[1]

    let coord_start = {'x': canvas_width / 2, 'y': border};

    for (let i = 0; i < bar_white; i++) {
        context.beginPath();
        context.arc(coord_start.x, coord_start.y + radius + 2 * i * radius, radius, 0, 2 * Math.PI);
        context.fillStyle = PLAYER_COLOR;
        context.fill();
        context.strokeStyle = STROKE_COLOR;
        context.stroke()
        if (i >= 3) {
            context.fillStyle = CANVAS_FILL_COLOR;
            context.fillText(bar_white, coord_start.x - 8, coord_start.y + radius + 2 * i * radius + 10);
            break;
        }

    }

    coord_start = {'x': canvas_width / 2, 'y': canvas_height - border};

    for (let i = 0; i < bar_black; i++) {

        context.beginPath();
        context.arc(coord_start.x, coord_start.y - radius - 2 * i * radius, radius, 0, 2 * Math.PI);
        context.fillStyle = CANVAS_FILL_COLOR;
        context.fill();
        context.strokeStyle = PLAYER_COLOR;
        context.stroke()
        if (i >= 3) {
            context.fillStyle = PLAYER_COLOR;
            context.fillText(bar_black, coord_start.x - 8, coord_start.y - radius - 2 * i * radius + 10);
            break;
        }

    }

}
