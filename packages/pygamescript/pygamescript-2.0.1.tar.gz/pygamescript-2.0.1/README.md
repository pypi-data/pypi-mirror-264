# Pure Python Game Script Frame
base `minidevice` and `minicv`
- Template
    - ImageTemplate
    - ColorsTemplate
- GameScript
    - screenshot -> cv2.Mat
    - saveScreenshot(path) 
    - find(Template,isColor=None,colorThreshold=4)
    - findAndOperate(Template,operate,operateParams)