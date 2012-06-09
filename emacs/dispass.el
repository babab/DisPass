;;; dispass.el --- Generate and disperse/dispell passwords

;; Copyright (C) 2012 Tom Willemsen <tom@ryuslash.org>

;; Author: Tom Willemsen <tom@ryuslash.org>
;; Created: Jun 8, 2012
;; Version: 0.1a7.2
;; Keywords: encryption, security

;; Permission to use, copy, modify, and distribute this software for any
;; purpose with or without fee is hereby granted, provided that the
;; above copyright notice and this permission notice appear in all
;; copies.

;; THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
;; WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
;; WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
;; AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
;; CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
;; OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
;; NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
;; CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

;;; Commentary:

;; dispass.el is an emacs wrapper around dispass
;; (http://dispass.babab.nl).

;;; Installation:

;; Place this file somewhere on your filesystem, either in your
;; `load-path' or somewhere else which you will have to add to your
;; `load-path', like so:

;;     (add-to-list 'load-path "/location/of/dispass.el")

;; And then `load', `require' or `autoload' it in your emacs init
;; file, for example:

;;     (require 'dispass)

;; _Or_ if you have package.el you could use `package-install-file'.

;;; Usage:

;; Using dispass.el is simple, once installed. Either call `dispass'
;; to recall a priviously generated password or call `dispass-create'
;; to generate a new password.

;; The only real difference between the two is that `dispass-create'
;; asks to confirm the password. Both will ask for a label.

;; Once a password has been generated it is inserted into the kill
;; ring and the system's clipboard so it can be easily inserted into
;; password field, this makes the generated password easy to see in
;; plaintext in the `kill-ring' variable, though.

;;; Change Log:

;; 0.1a7 - Initial release.

;; 0.1a7.1 - Don't show password, copy directly into the clipboard.

;; 0.1a7.2 - Kill buffer whenever we're finished with it.

;;; Code:

(defun dispass-process-sentinel (proc status)
  "Report PROC's status change to STATUS."
  (let ((status (substring status 0 -1))
        (buffer (process-buffer proc)))
    (unless (string-equal status "finished")
      (message "dispass %s" (substring status 0 -1)))

    (unless (eq (current-buffer) proc)
      (kill-buffer buffer))))

(defun dispass-erase-buffer (buffer)
  "Completely erase the contents of BUFFER"
  (save-current-buffer
    (set-buffer buffer)
    (buffer-disable-undo buffer)
    (kill-buffer buffer)))

(defun dispass-process-filter-for (label)
  "Create a function that will process any lines whilst keeping
an eye out for LABEL."
  `(lambda (proc string)
     "Process STRING coming from PROC."
     (cond ((string-match "^\\(Password\\|Again\\): ?$" string)
            (process-send-string proc
                                 (concat (read-passwd string nil) "\n")))

           ((string-match (concat "^[ ]+" ,label " \\(.\\{30\\}\\)$")
                          string)
            (let ((buffer (process-buffer proc)))
              (with-current-buffer buffer
                (insert (match-string 1 string))
                (clipboard-kill-ring-save (point-min) (point-max))
                (message "Password copied to clipboard.")

                (unless (eq (process-status proc) 'run)
                  (kill-buffer buffer))))))))

(defun dispass-start-process (label &optional create)
  "Start dispass process. When CREATE is non-nil send along the
  -c switch to make it ask for a password twice."
  (let ((proc (start-process "dispass" "*dispass*" "dispass"
                             (if create "-co" "-o") label)))
    (set-process-sentinel proc 'dispass-process-sentinel)
    (set-process-filter proc (dispass-process-filter-for label))))

;;;###autoload
(defun dispass-create (label)
  (interactive "MLabel: ")
  "Create a new password for LABEL."
  (dispass-start-process label t))

;;;###autoload
(defun dispass (label)
  (interactive "MLabel: ")
  "Recreate a password previously used."
  (dispass-start-process label))

(provide 'dispass)

;;; dispass.el ends here
