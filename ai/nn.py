import tensorflow as tf

mnist = tf.keras.datasets.mnist
(xtrain, ytrain), (xtest, ytest) = mnist.load_data()
xtrain = tf.keras.utils.normalize(xtrain, axis=1)
xtest = tf.keras.utils.normalize(xtest, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
##model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
##model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
##model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
##model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

model.add(tf.keras.layers.Dense(16, activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(16, activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=["accuracy"]  )
model.fit(xtrain, ytrain, epochs=10)

val_loss, val_acc = model.evaluate(xtest, ytest)
print(val_loss, val_acc)

##OBJECTIVE MET, 99% training accuracy, 97% test accuracy

##TODO refine to prevent overfitting, test iteratively
