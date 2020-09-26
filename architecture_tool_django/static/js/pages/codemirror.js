$(function () {
    var te_json = document.getElementById("textarea-codemirror");
    window.editor_json = CodeMirror.fromTextArea(te_json, {
        mode: "application/ld+json",
        theme: "monokai",
        lineNumbers: true,
        lineWrapping: true,
        matchBrackets: true,
        viewportMargin: Infinity,
        lint: true,
        autoCloseBrackets: true,
        extraKeys: {
            "Ctrl-Q": function (cm) {
                cm.foldCode(cm.getCursor());
            },
            "F7": function autoFormat(cm) {
                var totalLines = cm.lineCount();
                cm.autoFormatRange({
                    line: 0,
                    ch: 0
                }, {
                    line: totalLines
                });
            }
        },
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
        foldOptions: {
            widget: (from, to) => {
                var count = undefined;

                // Get open / close token
                var startToken = '{',
                    endToken = '}';
                var prevLine = window.editor_json.getLine(from.line);
                if (prevLine.lastIndexOf('[') > prevLine.lastIndexOf('{')) {
                    startToken = '[', endToken = ']';
                }

                // Get json content
                var internal = window.editor_json.getRange(from, to);
                var toParse = startToken + internal + endToken;

                // Get key count
                try {
                    var parsed = JSON.parse(toParse);
                    count = Object.keys(parsed).length;
                } catch (e) {}

                return count ? `\u21A4${count}\u21A6` : '\u2194';
            }
        }
    });

    editor_json.autoFormatRange({
        line: 0,
        ch: 0
    }, {
        line: editor_json.lineCount()
    });

    editor_json.foldCode(CodeMirror.Pos(1, 0));

    $('#format').on('click', function () {
        editor_json.autoFormatRange({
            line: 0,
            ch: 0
        }, {
            line: editor_json.lineCount()
        });
    })
})
