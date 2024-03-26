const BODY = document.querySelector("body"), SELECTORS = {
    "table": "table#cells",
    "body": "table#cells>tbody",
    "row": "table#cells>tbody>tr",
    "header": "table#cells>tbody>tr>th",
    "cell": "table#cells>tbody>tr>td",
}, ROLES = {
    "list": {
        "table": "presentation",
        "body": "list",
        "row": "listitem",
        "header": "none",
        "cell": "none",
    }, "table": {
        "table": "table",
        "body": "rowgroup",
        "row": "row",
        "header": "rowheader",
        "cell": "cell",
    }, "region": {
        "table": "presentation",
        "body": "presentation",
        "row": "region",
        "header": "none",
        "cell": "none",
    }, "presentation": {
        "table": "presentation",
        "body": "none",
        "row": "none",
        "header": "none",
        "cell": "none",
    }
};

function toggleColorScheme(value = null) {
    value = document.forms.settings.elements["color-scheme"].value;
    let DARK = value == "dark";
    let opposite = DARK ? "light" : "dark";
    document.getElementById(`nb-${value}-highlight`).removeAttribute("media", "screen");
    document.getElementById(`nb-${opposite}-highlight`).setAttribute("media", "not screen");
    document.querySelector(`head > meta[name="color-scheme"]`).setAttribute("content", value);
    BODY.classList.toggle("dark", DARK);
    activityLog(`${value} mode activated`)
}
function toggleRole() {
    let value = document.forms.settings["cell-navigation"].value;
    for (const [k, selector] of Object.entries(SELECTORS)) {
        document.querySelectorAll(selector).forEach(
            (x) => {
                if (ROLES[value][k] == null) {
                    x.removeAttribute("role")
                } else {
                    x.setAttribute("role", ROLES[value][k])
                }
            }
        );
    }
    activityLog(`notebook cell navigation set to ${event.target.value}.`);
}
function flattenCss(x) {
    return Object.entries(x).map(x => x.join(": ")).join("; ");
}
function getStyle() {
    return {
        "--nb-font-size": document.forms.settings["font-size"].value,
        "--nb-font-family": document.forms.settings["font-family"].value,
        "--nb-margin": `${document.forms.settings.elements.margin.value}%`,
        "--nb-line-height": `${document.forms.settings.elements["line-height"].value}`,
    }
}
function setStyle(msg) {
    BODY.setAttribute("style", flattenCss(getStyle()));
    setWCAG(); toggleColorScheme(); toggleColorScheme();
    activityLog(msg);
}
function changeFont() {
    document.forms.settings["font-size"].value;
    setStyle(`font size change`);
}
function changeFontFamily() {
    let value = document.forms.settings["font-family"].value;
    setStyle(value == "serif" ? `serifs included` : `serifs removed`)
}
function activityLog(msg, silent = false, first = false) {
    document.querySelectorAll("details.log+table").forEach(
        (body, i) => {
            let tr = document.createElement("tr"),
                th = document.createElement("th"),
                time = document.createElement("time"),
                td = document.createElement("td"),
                out = document.createElement("output"),
                now = Date.now();
            time.setAttribute("datetime", now), th.setAttribute("aria-live", "off"), th.setAttribute("hidden", null);
            time.textContent = now;
            body.append(tr), th.append(time), tr.append(th), tr.append(td), td.append(out);
            silent ? out.setAttribute("aria-live", "off") : null;
            out.textContent = msg;
            if (!i && document.forms.settings.elements["synthetic-speech"].checked) {
                // a non-screen reader solution for audible activity.
                speechSynthesis.speak(new SpeechSynthesisUtterance(msg));
            }
        }
    );
};
function openDialog() {
    event.preventDefault();
    document.getElementById(event.target.getAttribute("aria-controls")).showModal();
};
const L = 37, U = 38, R = 39, D = 40;
document.querySelectorAll("table[role=grid]").forEach(
    (x) => {
        x.addEventListener("keydown", (e) => {
            let target = document.activeElement;
            let i = Array.prototype.indexOf.call(target.parentElement.parentElement.childNodes, target.parentElement);
            switch (e.code) {
                case L:
                    break
                case U:
                    break
                case R:
                    break
                case D:
                    break
            };
        })
    }
);
document.forms.settings.elements["cell-navigation"].addEventListener("change", toggleRole)

document.forms.settings.elements["color-scheme"].addEventListener("change", toggleColorScheme);
document.forms.settings.elements["font-size"].addEventListener("change", (x) => {
    setStyle("change font size");
});
document.forms.settings.elements["font-family"].addEventListener("change", changeFontFamily);
document.forms.settings.elements["synthetic-speech"].addEventListener("change", (x) => {
    activityLog("speech on")
});
document.forms.settings.elements.margin.addEventListener("change", (x) => {
    setStyle("margin changed");
});
document.forms.settings.elements["line-height"].addEventListener("change", (x) => {
    setStyle("line height changed");
});
function setWCAG() {
    var priority = document.forms.settings["accessibility-priority"].value.toLowerCase();
    ["a", "aa", "aaa"].forEach(
        (x) => {
            if (x == priority) {
                BODY.classList.add(`wcag-${x}`)
            } else {
                BODY.classList.remove(`wcag-${x}`)
            }
        }
    );
}
document.forms.settings.elements["accessibility-priority"].addEventListener("change", setWCAG);
function toggleActive() {
    if (document.forms.notebook.elements.edit.checked) {
        document.querySelectorAll("tr.cell>td>details>summary[inert]").forEach(
            x => x.removeAttribute("inert")
        );
        document.querySelectorAll("tr.cell>td>details>textarea[readonly]").forEach(
            x => x.removeAttribute("readonly")
        );
        document.querySelectorAll("tr.cell>td>form").forEach(
            x => x.removeAttribute("hidden")
        );
        activityLog("entering edit mode");
    } else {
        document.querySelectorAll("tr.cell>td>details>summary").forEach(
            x => x.setAttribute("inert", null)
        );
        document.querySelectorAll("tr.cell>td>details>textarea").forEach(
            x => x.setAttribute("readonly", null)
        );
        document.querySelectorAll("tr.cell>td>form").forEach(
            x => x.setAttribute("hidden", null)
        );
        activityLog("entering reading mode");
    }
}


document.forms.notebook.elements.edit.addEventListener("change", () => toggleActive())

function openDialogs() {
    let trigger = document.querySelector("#nb-dialogs > details");
    Array.from(
        document.querySelectorAll("#nb-dialogs dialog:not(.log)")
    ).reverse().forEach(
        x => {
            trigger.getAttribute("open") === null ? x.show() : x.close();
        }
    );
    event.target.focus();
}

document.forms.visibility['visually-hide'].addEventListener("change",
    (x) => {
        document.querySelector("main").classList.toggle("visually-hide");
        activityLog(`${event.target.checked ? "hiding" : "showing"} main content`);
    });

document.forms.settings['horizontal-scrolling'].addEventListener("change",
    (x) => {
        BODY.classList.toggle("horiz-overflow", event.target.checked);
        if (!event.target.checked) {
            document.querySelectorAll("textarea").forEach(
                (x) => {
                    x.style.width = "";
                    x.style.height = "";
                }
            )
        };
        // activityLog(`${event.target.checked ? "overflow scrol" : "showing"} main content`);
    });

document.forms.visibility["accessibility-audit"].addEventListener("change", (event) => {
    document.getElementsByTagName("body")[0].toggleAttribute("data-dev-sa11y", event.target.checked);
});


function fullScreen() {
    if (!document.fullscreenElement) {
        document.querySelector("main").requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

// resizing hits the width before the height.
// width resizes trigger height resizes and height resizes need to be computed from scratch.
// we handle that logic with boolean flags when sets the width/height.
function setTextareaWidth(entry, set = null) {
    if (set === null) { return }
    if (set) {
        entry.target.style.width = "";
        let props = getComputedStyle(entry.target);
        let width = entry.target.scrollWidth,
            left = Number(props.borderLeftWidth.slice(0, -2)),
            right = Number(props.borderRightWidth.slice(0, -2));
        entry.target.style.width = `${Math.floor(width)}px`
        setTextareaHeight(entry, true);
    }
}

function setTextareaHeight(entry, reset = null) {
    if (reset === null) { return }
    let props = getComputedStyle(entry.target);
    if (reset) {
        entry.target.style.height = ""
        return setTextareaHeight(entry, false)
    } else {
        let height = entry.target.scrollHeight;
        let top = Number(props.borderTopWidth.slice(0, -2));
        let bottom = Number(props.borderBottomWidth.slice(0, -2));
        entry.target.style.height = `${Math.ceil(height) + Math.ceil(top) + Math.ceil(bottom) + 1}px`;
    }

}
let observer = new ResizeObserver(
    (entries) => {
        entries.forEach((entry) => {
            (BODY.matches(".horiz-overflow") ? setTextareaWidth : setTextareaHeight)(entry, true);
        });
    }
);

document.querySelectorAll("textarea").forEach(
    (x) => {
        observer.observe(x);
    }
);

if (!document.fullscreenEnabled) {
    document.getElementById("nb-fullscreen").setAttribute("hidden", "");
}

setStyle("initialize saved settings.")
// async function runSource(target) {
//     {
//         let pyodide = await loadPyodide();
//         pyodide.runPython(target.elements.source.value).then(
//             (x) => {
//                 console.log(x)
//             }, (x) => {
//                 console.log(x)
//             }
//         )
//         return false;
//     }
// }
// document.querySelectorAll("form.nb-toolbar").forEach((x) => {
//     x.addEventListener("submit", (event) => {
//         event.preventDefault();
//     })
// });
// document.querySelectorAll("textarea[name=source]").forEach(
//     (x) => {
//         x.addEventListener("keydown", (event) => {
//             if (event.ctrlKey && event.key === 'Enter') {
//                 runSource(event.target.form);
//             }
//         })
//     }
// );