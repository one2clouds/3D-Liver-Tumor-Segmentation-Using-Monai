import pandas as pd
from monai.transforms import (AsDiscreted,RandShiftIntensityd,RandScaleIntensityd,ScaleIntensity,NormalizeIntensityd,Compose,ScaleIntensityd, Spacingd, Transform, EnsureChannelFirstd,AsChannelLast,LoadImaged, RandSpatialCropd, RandGaussianNoised,SpatialPadd,RandSpatialCropd,RandFlipd,EnsureTyped)
from monai.inferers import AvgMerger,SlidingWindowInferer,SliceInferer, PatchInferer, WSISlidingWindowSplitter, SlidingWindowSplitter

def testing_model():
    test_transforms = Compose([
            LoadImaged(keys=['image', 'seg'],image_only=False),
            EnsureChannelFirstd(keys=['image', 'seg']),    
            #     RandSpatialCropd(['image', 'seg'],roi_size=(128, 128, 128), random_size=False),
            ScaleIntensityd(keys='image',channel_wise=False)])

    # WSI Reader backend
    WSI_BACKEND = "cucim"
    # TODO
    patch_size = 128 #64
    # pad_mode =  allows you to specify different ways to perform padding = None or constant
    # match_spatial_shape = True means to crop the output to match the input shape

    # inferer = SlidingWindowInferer(roi_size = (64,64,64),overlap=0.25)


    inferer = PatchInferer(
                splitter=SlidingWindowSplitter(patch_size=patch_size,overlap = 10, pad_mode="constant"),
    #             splitter=WSISlidingWindowSplitter(patch_size=patch_size,overlap = 10, pad_mode="constant", reader=WSI_BACKEND, level=6),
                merger_cls=AvgMerger,
                match_spatial_shape=True,
            )
    model.to('cpu')
    file_name_test_after_transform, test_outputs = run_inference(inferer, model, file_names_test,test_transforms)




def run_inference(inferer, model, filenames_test, test_transforms):
    outputs=[]
    file_name_test_after_transform = test_transforms(filenames_test)
#     print(file_name_test_after_transform[0]['image'].unsqueeze(dim=0).cuda())
    for index in tqdm(range(len(file_name_test_after_transform))):
        image = file_name_test_after_transform[index]["image"].unsqueeze(dim=0)
#         print(image.max(), image.min())
#         print(image.is_cuda, next(model.parameters()).is_cuda)
        out_image = inferer(inputs=image,network=model)
#         print(out_image.shape)
        out_image_soft = nn.Softmax(dim=1)(out_image)
#         print(out_image_soft.max(), out_image_soft.min())
        outputs.append(out_image_soft)
    return file_name_test_after_transform, outputs











if __name__=='__name__':
    df = pd.read_csv('test_dataset.csv')
    images_list_test = list(df.image)
    segmentation_list_test = list(df.segmentation)

    file_names_test = []
    for i in range(len(images_list_test)):
        file_names_test.append({"image":images_list_test[i], "seg":segmentation_list_test[i]})

    
    testing_model()













