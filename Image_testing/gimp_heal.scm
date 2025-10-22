; GIMP Script-Fu to remove watermarks
(let* ((input-file "E:/Github/Python_Testing/Image_testing/Images/2025_2C.jpg")
       (mask-file "E:/Github/Python_Testing/Image_testing/Images/2025_2C_patchmatch_mask.jpg")
       (output-file "E:/Github/Python_Testing/Image_testing/Images/2025_2C_gimp.jpg")
       (image (car (gimp-file-load RUN-NONINTERACTIVE input-file input-file)))
       (drawable (car (gimp-image-get-active-layer image)))
       (mask-image (car (gimp-file-load RUN-NONINTERACTIVE mask-file mask-file)))
       (mask-layer (car (gimp-image-get-active-layer mask-image))))
  
  ; Insert mask as a layer
  (gimp-image-insert-layer image mask-layer 0 0)
  
  ; Select by color (white in mask)
  (gimp-image-select-color image CHANNEL-OP-REPLACE mask-layer '(255 255 255))
  
  ; Remove mask layer
  (gimp-image-remove-layer image mask-layer)
  (gimp-image-delete mask-image)
  
  ; Apply healing/resynth if available, otherwise use remove selection
  (if (defined? 'plug-in-resynthesizer)
      (plug-in-resynthesizer RUN-NONINTERACTIVE image drawable 0 0 1 9 9 0.0 0.117 16 500)
      (gimp-context-set-sample-merged TRUE)
      )
  
  ; Flatten and save
  (set! drawable (car (gimp-image-flatten image)))
  (file-jpeg-save RUN-NONINTERACTIVE image drawable output-file output-file 0.95 0 1 1 "" 0 1 0 0)
  
  ; Clean up
  (gimp-image-delete image)
  (gimp-quit 0))
